# coding=utf-8

"""
    author : youfaNi
    date : 2016-10-31
"""
import pdb
import psycopg2
from tornado.options import options

try:
    host = options.host
    port = options.port
    user = options.user
    password = options.password
except:
    host = "localhost"
    port = 5432
    user = "odoo"
    password = ""

conn = None

def get_connect(database):
    global conn
    if conn:
        return conn
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    return conn

if __name__ == "__main__":
    conn = get_connect("community")
    cr = conn.cursor()

    cr.execute("select id, name, create_date from odootask_unit")
    objs = cr.fetchall()
    print objs

    cr.execute("select id, name, create_date from odootask_unit")
    obj = cr.fetchone()
    print obj

    conn.commit()
    conn.close()