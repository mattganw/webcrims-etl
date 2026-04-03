import os
from mssql_python import connect
from dotenv import load_dotenv

load_dotenv()
DB_CONN_STR = os.getenv("DB_CONNECTION_STRING")

def connect_to_db():
    try:
        conn = connect(DB_CONN_STR)
        return conn
    except Exception:
        raise
    
if __name__ == "__main__":
    pass