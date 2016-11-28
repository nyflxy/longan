# -*- coding: utf-8 -*-

"""
    alter by: Daemon
    alter on 2016-08-10
"""

import os
import platform
import sys
import pdb
from tornado.options import define, options, parse_command_line
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding('utf-8')

if platform.system() == "Linux":
    os.environ["PYTHON_EGG_CACHE"] = "/tmp/egg"

_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(_root))

import addons

os.chdir(_root)
import tornado
from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
import dxb
import libs
from libs.options import parse_options
from dxb import consts

class Application(web.Application):
    def __init__(self):
        from dxb.urls import handlers, ui_modules

        settings = dict(debug=options.debug,
                        template_path=os.path.join(os.path.dirname(__file__),
                                                   "static/www"),
                        static_path=os.path.join(os.path.dirname(__file__),
                                                 "static"),
                        login_url=options.login_url,
                        xsrf_cookies=options.xsrf_cookies,
                        cookie_secret=options.cookie_secret,
                        ui_modules=ui_modules,
                        #autoescape=None,
                        )

        super(Application, self).__init__(handlers, **settings)

        # 建议设定为CPU核心数量 * 4或8或16也是可以接受的, 取决于计算量，计算量越大设定的值应该越小.
        self.executor = tornado.concurrent.futures.ThreadPoolExecutor(16)

    def reverse_api(self, request):
        """Returns a URL name for a request"""
        handlers = self._get_host_handlers(request)

        for spec in handlers:
            match = spec.regex.match(request.path)
            if match:
                return spec.name

        return None

def main():
    parse_options()
    http_server = HTTPServer(Application())
    http_server.listen(options.port)
    print ("\nserver start !")
    print ("port:%s"%options.port)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
