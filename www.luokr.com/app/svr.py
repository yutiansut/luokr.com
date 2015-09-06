#coding=utf-8

import os.path, sys
reload(sys)
sys.setdefaultencoding('utf-8')

TOP_DIR = os.path.dirname(sys.path[0])
sys.path[0] = TOP_DIR
sys.path.insert(1, os.path.join(TOP_DIR, 'lib'))

import tornado.web
from tornado.options import define, options
from app.url import url
from app.etc import etc

app = tornado.web.Application(handlers = url, **etc)

define("port", default=8001, help="run on the given port", type=int)
def main():
    options.parse_command_line()
    print("Starting tornado web server on http://127.0.0.1:%s" % options.port)
    print("Quit the server with CONTROL-C")
    app.listen(options.port, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
