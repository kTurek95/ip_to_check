def add_ip(db_connection, ip: str):
    """
    Inserts the provided IP address into the 'ip_to_check' database.

    Args:
        db_connection (sqlite3.Connection): The database connection.
        ip (str): The IP address to be inserted into the database.
    """
    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO ip_to_check VALUES(?)', (
        (ip,)
    ))
    db_connection.commit()


def get_ips(db_connection):
    """
    Retrieves a list of IP addresses from the 'ip_to_check' database.

    Args:
        db_connection (sqlite3.Connection): The database connection.

    Returns:
        sqlite3.Cursor: A cursor object containing the result set.
            Use this cursor to iterate over the IP addresses retrieved from the database.
    """
    cursor = db_connection.cursor()
    res = cursor.execute('SELECT ip FROM ip_to_check')

    return res


def save_status(db_connection, ip: str, is_up: bool):
    """
    Inserts the status of an IP address into the 'log' table of the database.

    Args:
        db_connection (sqlite3.Connection): The database connection.
        ip (str): The IP address for which the status is being saved.
        is_up (bool): The status of the IP address (True for 'up', False for 'down').
    """

    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO log(ip, is_up) VALUES(?, ?)', (
        ip,
        int(is_up)
    ))
    db_connection.commit()


def initialize(db_connection):
    """
    Initializes the database with required tables if they do not exist.

    Args:
        db_connection (sqlite3.Connection): The database connection.

    """
    sqls = ['''CREATE TABLE IF NOT EXISTS ip_to_check(
    ip TEXT
    )''', ''' CREATE TABLE IF NOT EXISTS log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip TEXT,
    is_up INTEGER
    )''']
    cursor = db_connection.cursor()

    for sql in sqls:
        cursor.execute(sql)

    db_connection.commit()
