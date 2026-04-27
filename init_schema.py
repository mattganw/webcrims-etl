from database import DBSchema
from database import MSSQLConnection
from config import Settings

""" Helper to handle schema intialization """

if __name__ == '__main__':
    settings = Settings()
    conn = MSSQLConnection(settings.db_connection_string)
    schema = DBSchema(conn)

    schema.create_tables()