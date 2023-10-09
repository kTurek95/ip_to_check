import sqlite3
from database import initialize, add_ip, get_ips, save_status
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
        initialize(connection)

        while True:
            ip = input('Enter an IP address: ')
            if ip == 'end':
                break
            add_ip(connection, ip)

        for ip, in get_ips(connection):
            if not check_if_is_up(ip):
                print(f'Your ip adress "{ip}" is not valid')
        print('---' * 20)

        for ip, in get_ips(connection):
            save_status(connection, ip, check_if_is_up(ip))


if __name__ == '__main__':
    main()
