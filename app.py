from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from auth import autenticar
from queries import query_vendas
from database import execute_query

app = Flask(__name__)
app.secret_key = "chave-super-secreta-123"  # depois podemos melhorar


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