import sqlite3

from flask import app

def get_db():
    conn = sqlite3.connect('users.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()

def get_mail(usrname):
    conn=get_db()
    cursor = conn.cursor()
    username = usrname
    query = "SELECT email FROM users_details WHERE username='{}'".format(username)
    cursor.execute(query)
    rows = cursor.fetchall()
    print("email",rows)
    return rows
