import sqlite3
from sys import argv

from function import initialize, add_ip, get_ips, save_status, check_if_is_up


def main():
    with sqlite3.connect('ip_to_check.db') as connection:
        initialize(connection)

        while True:
            ip = input('Podaj adres ip: ')
            if ip == 'koniec':
                break
            add_ip(connection, ip)

        for ip, in get_ips(connection):
            print(ip)
        print('---' * 20)

        for ip, in get_ips(connection):
            save_status(connection, ip, check_if_is_up(ip))


if __name__ == '__main__':
    main()

