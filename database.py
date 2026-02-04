import os
import pyodbc
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    connection_string = (
        "DRIVER={SQL Server};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD}"
    )
    return pyodbc.connect(connection_string)


def execute_query(sql):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    resultado = []
    for row in rows:
        resultado.append(dict(zip(columns, row)))

    cursor.close()
    conn.close()

    return resultado


# Teste direto pelo terminal
if __name__ == "__main__":
    print("TESTE INICIADO")

    sql = "SELECT COUNT(*) AS total FROM MOINHO.dbo.cliente"
    resultado = execute_query(sql)

    print("RESULTADO:", resultado)