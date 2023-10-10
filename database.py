"""
Database Module

This module provides functionality for storing and logging IP addresses in a SQLite database.

It contains the following components:
- The 'Database' class:
  - Manages database operations such as inserting IP addresses, retrieving IP addresses, saving IP status, and initializing the database.
- A SQLite database connection is required before using this module.
- Ensure that the 'ip_to_check.db' SQLite database file exists in the same directory as this module.

Classes:
- Database: A class for handling database operations.

"""


class Database:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_ip(self, ip: str):
        """
            Inserts the provided IP address into the 'ip_to_check' database.

            Args:
                self.db_connection (sqlite3.Connection): The database connection.
                ip (str): The IP address to be inserted into the database.
            """
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO ip_to_check VALUES(?)', (
            (ip,)
        ))
        self.db_connection.commit()

    def get_ips(self):
        """
        Retrieves a list of IP addresses from the 'ip_to_check' database.

        Args:
            self.db_connection (sqlite3.Connection): The database connection.

        Returns:
            sqlite3.Cursor: A cursor object containing the result set.
                Use this cursor to iterate over the IP addresses retrieved from the database.
        """
        cursor = self.db_connection.cursor()
        res = cursor.execute('SELECT domain_name FROM ip_to_check')

        return res

    def save_status(self, ip: str, is_up: bool):
        """
        Inserts the status of an IP address into the 'log' table of the database.

        Args:
            self.db_connection (sqlite3.Connection): The database connection.
            ip (str): The IP address for which the status is being saved.
            is_up (bool): The status of the IP address (True for 'up', False for 'down').
        """

        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO log(domain_name, is_up) VALUES(?, ?)', (
            ip,
            int(is_up)
        ))
        self.db_connection.commit()

    def initialize(self):
        """
        Initializes the database with required tables if they do not exist.

        Args:
            self.db_connection (sqlite3.Connection): The database connection.

        """
        sqls = ['''CREATE TABLE IF NOT EXISTS ip_to_check(
        domain_name TEXT
        )''', ''' CREATE TABLE IF NOT EXISTS log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        domain_name TEXT,
        is_up INTEGER
        )''']
        cursor = self.db_connection.cursor()

        for sql in sqls:
            cursor.execute(sql)

        self.db_connection.commit()
