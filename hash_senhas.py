import pandas as pd
from werkzeug.security import generate_password_hash

ARQUIVO = "usuarios.xlsx"

df = pd.read_excel(ARQUIVO)

# gera hash
df["senha"] = df["senha"].astype(str).apply(
    lambda x: generate_password_hash(x)
)

df.to_excel(ARQUIVO, index=False)

print("✅ Senhas criptografadas com sucesso")