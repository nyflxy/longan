# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-07-14
# Alter by nyf
#

from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import IOLoop
from tornado.concurrent import run_on_executor

class AsyncUtils(object):
    def __init__(self,num_worker=8):
        self.io_loop = IOLoop.current()
        self.executor = ThreadPoolExecutor(num_worker)

    @run_on_executor
    def cmd(self,func, *args, **kwargs):
        res = func(*args,**kwargs)
        return res

import tornado.httpclient
import tornado.web
import tornado.gen
import tornado.ioloop
import tornado.options
import tornado.httpserver
import requests
import pdb

class BlockingHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # 如果这条命令没看懂的话，请参考这个链接: http://www.tornadoweb.org/en/stable/faq.html
        yield tornado.gen.sleep(3)
        self.write('ok')

class NonBlockHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.write('non_blocking')

class BlockHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        response = requests.get('http://localhost:8888/blocking')     # blocked here.
        result = dict(response.headers)
        result.update({'content': response.content})
        self.write(result)

class Block2Handler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch('http://localhost:8888/blocking', callback=self.on_response)

    def on_response(self, content):
        result = dict(content.headers)
        result.update({'content': content.body})
        self.write(result)
        self.finish()

class Block3Handler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):                          # def get上方移除了tornado.web.asynchonous装饰器
        client = tornado.httpclient.AsyncHTTPClient()
        future = client.fetch('http://localhost:8888/blocking')                    # 在这里添加callback也行
        tornado.ioloop.IOLoop.current().add_future(future, callback=self.on_response)

    def on_response(self, content):
        result = dict(content.headers)
        result.update({'content': content.body})
        self.write(result)
        self.finish()

class Block4Handler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        client = tornado.httpclient.AsyncHTTPClient()
        future = tornado.concurrent.Future()
        fetch_future = client.fetch('http://localhost:8888/blocking', callback=self.on_response)
        fetch_future.add_done_callback(lambda x: future.set_result(x.result()))

    def on_response(self, content):
        result = dict(content.headers)
        result.update({'content': content.body})
        self.write(result)
        self.finish()

class Block5Handler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        client = tornado.httpclient.AsyncHTTPClient()
        content = yield tornado.gen.Task(client.fetch, ('http://localhost:8888/blocking'))
        result = dict(content.headers)
        result.update({'content': content.body})
        self.write(result)
        self.finish()

class Block6Handler(tornado.web.RequestHandler):

    @property
    def executor(self):
        return self.application.executor

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        print dir(self)
        content = yield self.executor.submit(requests.get, ('http://localhost:8888/blocking'))
        result = dict(content.headers)
        result.update({'content': content.content})
        self.write(result)
        self.finish()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/blocking', BlockingHandler),
            ('/block', Block6Handler),
            ('/non_block', NonBlockHandler),
        ]
        super(Application, self).__init__(handlers)
        # 建议设定为CPU核心数量 * 4或8或16也是可以接受的, 取决于计算量，计算量越大设定的值应该越小.
        self.executor = tornado.concurrent.futures.ThreadPoolExecutor(16)

if __name__ == "__main__":
    tornado.options.define("port", default=8888, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
    
def exception_handler(func):

    def handler(self,*args,**kwargs):
        try:
            future = func(self,*args,**kwargs)
            if future.exc_info():
                raise Exception(future.result())
        except Exception, e:
            pdb.set_trace()
            result = utils.init_response_data()
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
    return handler

class TestHandler(tornado.web.RequestHandler):
    model = models.LinkModel()

    @exception_handler
    @tornado.gen.coroutine
    def get(self):
        result = utils.init_response_data()
        self.finish(result)
        yield self.application.executor.submit(self.print_name,("name"))

    def print_name(self,name):
            print name
