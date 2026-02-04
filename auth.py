import pandas as pd
from werkzeug.security import check_password_hash

USUARIOS_ARQUIVO = "usuarios.xlsx"

GERENCIA = {
    "usuario": "admin",
    "senha": "admin@2024",
    "perfil": "gerencia"
}

def autenticar(usuario, senha):
    # GERÊNCIA
    if usuario == GERENCIA["usuario"] and senha == GERENCIA["senha"]:
        return {
            "usuario": usuario,
            "perfil": "gerencia"
        }

    # USUÁRIOS DO EXCEL
    df = pd.read_excel(USUARIOS_ARQUIVO, dtype=str)

    user = df[df["usuario"] == str(usuario)]

    if user.empty:
        return None

    senha_hash = user.iloc[0]["senha"]

    if check_password_hash(senha_hash, senha):
        return {
            "usuario": user.iloc[0]["usuario"],
            "perfil": user.iloc[0]["perfil"]
        }

    return None