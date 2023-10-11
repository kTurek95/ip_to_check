"""
IP Address Checking and Logging Module.

This module provides functionality for checking the validity of IP addresses and logging their status in a database.

It contains the following components:
- The 'main' function:
  - Initializes a SQLite database.
  - Continuously prompts the user to enter an IP address until 'end' is entered.
  - Checks the validity of each IP address.
  - Logs the status of each IP address in the database.
"""
import sqlite3
from database import Database
from ip import check_if_is_up


def main():
    """
    Main function for IP address checking and logging.

    This function:
    1. Initializes the database.
    2. Continuously prompts the user to enter an IP address until 'end' is entered.
    3. Checks the validity of each IP address.
    4. Logs the status of each IP address in the database.
    """
    with sqlite3.connect('ip_to_check.db') as connection:
        database = Database(connection)
        database.initialize()

        while True:
            ip = input('Enter an IP address: ')
            if ip == 'end':
                break
            database.add_ip(ip)

        for ip, in database.get_ips():
            if not check_if_is_up(ip):
                print(f'Your ip address "{ip}" is not valid')
        print('---' * 20)

        for ip, in database.get_ips():
            database.save_status(ip, check_if_is_up(ip))


if __name__ == '__main__':
    main()
