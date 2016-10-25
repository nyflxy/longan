#coding=utf-8

"""
    tornado 非阻塞异步和协程实现原理

"""

#主要模块
import tornado
from tornado import web
from tornado import escape
from tornado import template
from tornado import httpclient
from tornado import auth
from tornado import locale
from tornado import options
import torndb

#底层模块
from tornado import httpserver
from tornado import iostream
from tornado import ioloop
from tornado import util
import pdb


# tornado app
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class ProfileHandler(web.RequestHandler):

    def initialize(self, database):
        self.database = database

    def get(self, username):
        self.write("user")

# if __name__ == "__main__":
#     application = tornado.web.Application([
#         (r"/", MainHandler),
#         (r'/user/(.*)', ProfileHandler, dict(database=None)),
#     ])
#     application.listen(8888)
#     tornado.ioloop.IOLoop.current().start()


# python TCP Server 实现
# server
def server():
    import socket
    while True:
        address = ('127.0.0.1', 31500)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # s = socket.socket()
        s.bind(address)
        s.listen(5)

        ss, addr = s.accept()
        print 'got connected from', addr


        ra = ss.recv(512)
        print ra
        if ra == "hihi":
            ss.send('byebye')
        else:
            ss.send("hello")

        ss.close()
        s.close()

# client
def client():
    import socket

    address = ('127.0.0.1', 31500)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    s.send('hihi')
    data = s.recv(512)
    print 'the data received is', data

    s.close()

# ioloop事件循环 TCP Server + tornado.ioloop source code
import errno
import functools
import tornado.ioloop
import socket

def handle_connection(*args,**kwargs):
    connection = args[0]
    address = args[1]
    print address
    try:
        data = connection.recv(1024*10)
    except:
        pass
    connection.send(data)
    connection.close()

def connection_ready(sock, fd, events):
    while True:
        try:
            connection, address = sock.accept()
        except socket.error as e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        connection.setblocking(0)
        handle_connection(connection, address)


# if __name__ == '__main__':
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     sock.setblocking(0)
#     sock.bind(("", 8888))
#     sock.listen(128)
#
#     io_loop = tornado.ioloop.IOLoop.current()
#     callback = functools.partial(connection_ready, sock)
#     io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
#     print "server start!"
#     io_loop.start()


# tornado 协程

import tornado.ioloop
from tornado.gen import coroutine
from tornado.concurrent import Future

@coroutine
def asyn_sum(a, b):
    print("begin calculate:sum %d+%d"%(a,b))
    future = Future()

    def callback(a, b):
        print("calculating the sum of %d+%d:"%(a,b))
        future.set_result(a+b)
    tornado.ioloop.IOLoop.instance().add_callback(callback, a, b)

    result = yield future

    print("after yielded")
    print("the %d+%d=%d"%(a, b, result))

def main():
    asyn_sum(2,3)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()