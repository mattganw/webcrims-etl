from database import MSSQLConnection
from database import DBSchema


if __name__ == "__main__":
    conn = MSSQLConnection()
    schema = DBSchema(conn)
    schema.create_tables()