import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from auth import autenticar, criar_usuario_supabase, remover_usuario_supabase
from queries import query_vendas
from database import execute_query, get_supabase_client

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "chave-super-secreta-123")  # pode ser configurada via env


# ----------------------
# Rotas administrativas (apenas para perfil 'gerencia')
# ----------------------
@app.route('/admin/usuarios', methods=['POST'])
def admin_create_usuario():
    if 'usuario' not in session or session.get('perfil') != 'gerencia':
        return jsonify({'erro': 'não autorizado'}), 403

    usuario = request.form.get('usuario') or request.json.get('usuario') if request.is_json else request.form.get('usuario')
    senha = request.form.get('senha') or request.json.get('senha') if request.is_json else request.form.get('senha')
    perfil = request.form.get('perfil') or request.json.get('perfil') if request.is_json else request.form.get('perfil') or 'vendedor'

    if not usuario or not senha:
        return jsonify({'erro': 'usuario e senha são obrigatórios'}), 400

    try:
        res = criar_usuario_supabase(usuario, senha, perfil=perfil)
        return jsonify({'ok': True, 'data': res}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/admin/usuarios/<usuario>', methods=['DELETE'])
def admin_delete_usuario(usuario):
    if 'usuario' not in session or session.get('perfil') != 'gerencia':
        return jsonify({'erro': 'não autorizado'}), 403

    try:
        res = remover_usuario_supabase(usuario)
        return jsonify({'ok': True, 'data': res}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500



@app.route('/health')
def health():
    """Health check endpoint. Verifica se o app está vivo e se o cliente Supabase está configurado."""
    try:
        client = get_supabase_client()
        supabase_ok = bool(client)
        return jsonify({"status": "ok", "supabase": supabase_ok})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500


@app.route("/", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        user = autenticar(usuario, senha)

        if user:
            session["usuario"] = user["usuario"]
            session["perfil"] = user["perfil"]
            return redirect(url_for("dashboard"))
        else:
            erro = "Usuário ou senha inválidos"

    return render_template("login.html", erro=erro)


@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


@app.route("/api/vendas")
def api_vendas():
    if "usuario" not in session:
        return jsonify({"erro": "não autorizado"}), 401

    perfil = session["perfil"]
    codigo = session["usuario"]

    # 📅 Datas vindas do frontend
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    # Tenta usar Supabase SDK + materialized view `mv_vendas_pedido` quando disponível
    try:
        client = get_supabase_client()
        if client:
            query = client.table("mv_vendas_pedido").select("*")

            # Filtro por perfil
            if perfil == "vendedor":
                query = query.eq("cd_vend", codigo)
            elif perfil == "supervisor":
                query = query.eq("cd_vend", codigo)  # ajuste conforme sua modelagem de supervisor

            # Filtro por datas
            if data_inicio:
                query = query.gte("dt_ped", data_inicio)
            if data_fim:
                query = query.lte("dt_ped", data_fim)

            # Ordenação
            query = query.order("dt_ped", desc=True)

            res = query.execute()
            dados = getattr(res, "data", [])
            return jsonify(dados)
    except Exception:
        # Se houver qualquer problema com o SDK, faz fallback para SQL bruto
        pass

    # Fallback: executar SQL tradicional (psycopg2/SQL Server conforme configuração)
    filtro = None

    if perfil == "vendedor":
        filtro = f"vendedor.cd_vend = '{codigo}'"

    elif perfil == "supervisor":
        filtro = f"vendedor_1.cd_vend = '{codigo}'"

    sql = query_vendas(
        filtro_perfil=filtro,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

    dados = execute_query(sql)

    return jsonify(dados)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)