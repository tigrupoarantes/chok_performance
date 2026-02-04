import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Preferência por DATABASE_URL (ex.: Supabase)
DATABASE_URL = os.getenv("DATABASE_URL")

# Suporte opcional ao SDK do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

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
    """Executa SQL bruto usando psycopg2 (compatível com Postgres/Supabase).

    Use este método quando precisar rodar queries complexas/join.
    """
    conn = get_connection()
    try:
        # RealDictCursor retorna dicionários (útil para jsonify)
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params or ())
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    finally:
        conn.close()


# ----------------------
# Helpers opcionais para Supabase (SDK)
# ----------------------
try:
    from supabase import create_client
except Exception:
    create_client = None


def get_supabase_client():
    """Retorna um cliente Supabase (se SUPABASE_URL e SUPABASE_KEY estiverem definidos).

    Retorna None se as credenciais não estiverem presentes ou se a biblioteca não estiver instalada.
    """
    if not (SUPABASE_URL and SUPABASE_KEY and create_client):
        return None

    return create_client(SUPABASE_URL, SUPABASE_KEY)


def list_table(table, limit=50):
    """Lista até `limit` registros de uma tabela via SDK do Supabase.

    Observação: esta função usa `.table(...).select(...)` e não executa SQL cru.
    Use `execute_query` quando precisar de joins/aggregações complexas.
    """
    client = get_supabase_client()
    if not client:
        raise RuntimeError("Supabase client não está configurado (verifique SUPABASE_URL e SUPABASE_KEY)")

    res = client.table(table).select("*").limit(limit).execute()
    # `res.data` normalmente contém a lista de registros retornados pelo supabase-py
    return getattr(res, "data", [])


# Teste direto pelo terminal
if __name__ == "__main__":
    print("TESTE INICIADO")

    # Teste via SQL
    sql = "SELECT COUNT(*) AS total FROM cliente"
    resultado_sql = execute_query(sql)

    print("RESULTADO SQL:", resultado_sql)

    # Teste via SDK (se configurado)
    client = get_supabase_client()
    if client:
        print("Teste via Supabase SDK: listando clientes (até 5)")
        print(list_table("cliente", limit=5))
    else:
        print("Supabase SDK não configurado")"},{ 