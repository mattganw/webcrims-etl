"""
MSSQLConnection class used to handle connections to the MSSQL db.
Instantiate to create a connection that can be used to perform your db operations.
"""

import os
from mssql_python import connect
from dotenv import load_dotenv

load_dotenv()

class MSSQLConnection:
    """
    Handles connection to an MSSQL database.
    """

    def __init__(self, conn_str: str | None = None):
        """
        Initialize with a connection string. If not provided, loads from env.
        """
        self.conn_str = conn_str or os.getenv("DB_CONNECTION_STRING")
        if not self.conn_str:
            raise ValueError("Connection string is missing.")

        self.connection = None

    def connect(self):
        """ Establishes a database connection """
        try:
            self.connection = connect(self.conn_str)
            return self.connection
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {e}") from e

    def close(self):
        """ Closes the connection if open """
        if self.connection:
            self.connection.close()
            self.connection = None

    def __enter__(self):
        """ Allows use with `with` statements """
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    