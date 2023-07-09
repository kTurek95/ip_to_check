import subprocess
import sqlite3
from sys import argv


def main():
    with sqlite3.connect('ip_to_check.db') as connection:
        if len(argv) == 2 and argv[1] == 'setup':
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


def add_ip(db_connection, ip: str):
    """ dodanie adresu ip do bazy danych ip_to_check"""
    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO ip_to_check(ip) VALUES(?)', (
        (ip,)
    ))
    db_connection.commit()


def get_ips(db_connection):
    """ funkcja pobierająca adresy ip """
    cursor = db_connection.cursor()
    res = cursor.execute('SELECT ip FROM ip_to_check')

    return res  # zwracamy res, żeby móc po nim iterować, przechodzić po jego wartościach


def save_status(db_connection, ip: str, is_up: bool):
    """ funkcja zapisująca ip oraz status (czy udało się sprawdzić ip, czy nie) """
    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO log(ip, is_up) VALUES(?, ?)', (
        ip,
        int(is_up)  # zamieniamy to na int, ponieważ gdy wynik będzie True, to zwróci nam 1, a gdy będzie False to 0
    ))
    db_connection.commit()


def check_if_is_up(ip: str) -> bool:
    output = subprocess.run([f'ping -c 1 {ip}'], capture_output=True, shell=True)
    if 'cannot resolve' in output.stderr.decode('utf8').lower():
        return False
    else:
        return True


def initialize(db_connection):
    """ funkcja tworząca dwie tabele, 1 z nich to ip_to_check, 2 to log """
    sqls = ['''CREATE TABLE ip_to_check(
    ip TEXT
    )''', ''' CREATE TABLE log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip TEXT,
    is_up INTEGER
    )''']
    cursor = db_connection.cursor()

    for sql in sqls:
        cursor.execute(sql)

    db_connection.commit()
