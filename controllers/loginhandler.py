import tornado.web
from apiclient.discovery import build

import os
import sys

from basehandler import *

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
if not path in sys.path:
    sys.path.insert(1, path)

from models import User

import json
import random
import hashlib
import hmac
import string
from string import letters
import sys
import datetime
import logging
import re
from tornado.escape import json_encode
from _mysql_exceptions import IntegrityError

class LoginHandler(BaseHandler):
  @classmethod
  def install(cls, handlers):
    handlers.append((r"/login", LoginHandler))
  
  def post(self):
    have_error = False
    self.username = self.json_args.get('username')
    self.password = self.json_args.get('password')
    params = dict()
    try:
      u = User.get(User.username == self.username)
      if valid_pw(self.username, self.password, u.password_hash):
        self.login(u)
        self.write(json.dumps({"msg": 'Successfully connected user.'}))
      else:
        params['error_msg'] = 'Invalid Crendential'
        self.write(json_encode(params))
        self.set_status(400)
    except User.DoesNotExist:
      params['error_msg'] = 'Invalid Crendential'
      self.write(json_encode(params))
      self.set_status(400)
    self.set_header("Content-Type", "application/json") 
