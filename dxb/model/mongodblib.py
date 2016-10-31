# coding=utf-8

"""
    author : youfaNi
    date : 2016-07-13
"""

import pymongo, pdb
import sys, os, re
from tornado.options import options
try:
    import importlib
except:
    from dxb.libs import importlib
try:
    host = options.host
    port = options.port
except:
    host = "localhost"
    port = 27017

client = None

def get_client(table_name):
    global host
    global port
    global client
    if client:
        return client
    else:
        host = host
        port = port
        client = pymongo.MongoClient(host, port)
        return client

def get_coll(name):
    db_name = name.split(".")[0]
    coll_name = name.split(".")[1]
    client = get_client(coll_name)
    db = client[db_name]
    coll = db[coll_name]
    return coll