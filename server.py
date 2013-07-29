import os.path
import inspect
import base64
import logging
import json 
import random
import string
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.template import Loader
import uuid
from pycket.session import SessionMixin
from controllers import RegisterHandler
from controllers import LoginHandler
from controllers import LogoutHandler
from controllers import ImageUploaderHandler
from controllers import PhotoHandler
from tornado.options import define, options

this_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])

define("port", default=8000, help="run on the given port", type=int)

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.ERROR)

APPLICATION_NAME = 'AppName' 

class IndexHandler(tornado.web.RequestHandler, SessionMixin):
  def get(self):
    loader = Loader(os.path.join(this_folder, "template"))
    templ = loader.load("index.html")
    self.write(templ.generate(APPLICATION_NAME=APPLICATION_NAME))

class JustinHandler(tornado.web.RequestHandler, SessionMixin):
  def get(self):
    loader = Loader(os.path.join(this_folder, "template"))
    templ = loader.load("justin.html")
    self.write(templ.generate())


class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
        (r"/", IndexHandler),
        (r"/justin", JustinHandler)
    ]
    settings = dict(
#      cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
      cookie_secret="asfasfasflasjflasfjalKJFHIUHDSFLKHSF",
      template_path=os.path.join(os.path.dirname(__file__), "template"),
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      xsrf_cookies=True,
      autoescape=None,
      debug=True,
    )
    RegisterHandler.install(handlers)
    LoginHandler.install(handlers)
    LogoutHandler.install(handlers)
    ImageUploaderHandler.install(handlers)
    PhotoHandler.install(handlers)

    tornado.web.Application.__init__(self, handlers, **settings)

def main():
  tornado.options.parse_command_line()
  app = Application()
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
