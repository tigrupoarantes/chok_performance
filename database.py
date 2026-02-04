import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Preferência por DATABASE_URL (ex.: Supabase)
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback para conexão antiga (SQL Server) caso DATABASE_URL não esteja definida
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    if DATABASE_URL:
        # Supabase fornece uma URL compatível com Postgres
        return psycopg2.connect(DATABASE_URL, sslmode="require")
    else:
        # Fallback: conectar via pyodbc ao SQL Server
        import pyodbc
        connection_string = (
            "DRIVER={SQL Server};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD}"
        )
        return pyodbc.connect(connection_string)


def execute_query(sql, params=None):
    conn = get_connection()
    try:
        # RealDictCursor retorna dicionários (útil para jsonify)
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params or ())
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    finally:
        conn.close()


# Teste direto pelo terminal
if __name__ == "__main__":
    print("TESTE INICIADO")

    sql = "SELECT COUNT(*) AS total FROM cliente"
    resultado = execute_query(sql)

    print("RESULTADO:", resultado)"},{ 