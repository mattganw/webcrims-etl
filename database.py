import os
from mssql_python import connect
from dotenv import load_dotenv

load_dotenv()
DB_CONN_STR = os.getenv("DB_CONNECTION_STRING")

def connect_to_db():
    """ Connects to SQL db """
    if not DB_CONN_STR:
        raise ValueError("Connection string missing.")
    try:
        return connect(DB_CONN_STR)
    except Exception as e:
        raise ConnectionError(f"Failed to connect to database: {e}") from e
    
if __name__ == "__main__":
    pass