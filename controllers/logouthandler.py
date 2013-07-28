import tornado.web

import os
import sys

from basehandler import *

import json
import sys
import datetime
import logging
from tornado.escape import json_encode

class LogoutHandler(BaseHandler):
  @classmethod
  def install(cls, handlers):
    handlers.append((r"/logout", LogoutHandler))
  
  def post(self):
    self.clear_cookie('user_id')
