import psycopg2

if __name__ == '__main__':
    con = psycopg2.connect(user='postgres', host='localhost', password='mysecretpassword')
    con.autocommit = True

    cur = con.cursor()
    cur.execute('CREATE DATABASE mosquitto_auth;')