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

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

class LoginHandler(BaseHandler, SessionMixin):
  @classmethod
  def install(cls, handlers):
    handlers.append((r"/login", LoginHandler))
  
  def check_xsrf_cookie(self):
    return True

  def prepare(self):
    if self.request.headers.get("Content-Type") == "application/json":
        self.json_args = json.loads(self.request.body)

  def post(self):
    have_error = False
    self.username = self.json_args.get('username')
    self.password = self.json_args.get('password')
    params = dict()
    try:
      u = User.get(User.username == self.username)
      if valid_pw(self.username, self.password, u.password_hash):
        self.write("Successful")
      else:
        params['error_msg'] = 'Invalid Crendential'
        self.write(json_encode(params))
        self.set_status(400)
    except User.DoesNotExist:
      params['error_msg'] = 'Invalid Crendential'
      self.write(json_encode(params))
      self.set_status(400)
    self.set_header("Content-Type", "application/json") 