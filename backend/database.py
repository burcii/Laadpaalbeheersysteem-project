import mysql.connector
from config import config


class Database:
    def __init__(self):
        """
        Initializes the database object.
        """
        self.mydb = None
        self.mycursor = None

    def connect(self):
        """
        Establishes a connection to the database.
        """
        self.mydb = mysql.connector.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        self.mycursor = self.mydb.cursor(dictionary=True, buffered=True)
        return self.mydb

    def close(self):
        """
        Closes the database connection.
        """
        if self.mycursor:
            self.mycursor.close()
        if self.mydb:
            self.mydb.close()

    def execute_query(self, query, params=None):
        """
        Executes a query on the database.

        :param query: SQL query
        :param params: Values to pass to the query if they were given separately
        """
        if params:
            self.mycursor.execute(query, params)
        else:
            self.mycursor.execute(query)

    def commit(self):
        """
        Commits the changes to the database.
        """
        if self.mydb:
            self.mydb.commit()

    def row_count(self):
        """
        Gives the number of rows in the database.

        :return: The row count of the query
        """
        return self.mycursor.rowcount

    def rollback(self):
        """
        Discards all changes to the database since the last commit.
        """
        if self.mydb:
            self.mydb.rollback()

    def fetch_results(self):
        """
        Fetches all rows from the result.

        :return: all rows from the result
        """
        return self.mycursor.fetchall()

    def fetch_one(self):
        """
        Fetches one row from the result.

        :return: one row from the result
        """
        return self.mycursor.fetchone()

    def __enter__(self):
        """
        Enters the context manager.

        :return: self
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the context manager.
        """
        self.close()
