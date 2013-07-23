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
import string
import sys
import datetime
import logging
import re
from tornado.escape import json_encode
from _mysql_exceptions import IntegrityError

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class RegisterHandler(BaseHandler, SessionMixin):
  @classmethod
  def install(cls, handlers):
    handlers.append((r"/register", RegisterHandler))
  
  def check_xsrf_cookie(self):
    return True

  def prepare(self):
    if self.request.headers.get("Content-Type") == "application/json":
        self.json_args = json.loads(self.request.body)

  def post(self):
    have_error = False
    self.username = self.json_args.get('username')
    self.password = self.json_args.get('password')
    self.verify = self.json_args.get('verify')
    self.email = self.json_args.get('email')

    params = dict(username = self.username,
                 email = self.email)

    if not valid_username(self.username):
      params['error_username'] = "That's not a valid username."
      have_error = True

    if not valid_password(self.password):
      params['error_password'] = "That wasn't a valid password."
      have_error = True
    elif self.password != self.verify:
      params['error_verify'] = "Your passwords didn't match."
      have_error = True

    if not valid_email(self.email):
      params['error_email'] = "That's not a valid email."
      have_error = True

    if have_error:
      self.write(json_encode(params));
      self.set_status(400)
    else:
      try:
        u = User.get(User.username == self.username)
        params['error_username'] = "That user already exists."
        self.write(json_encode(params))
        self.set_status(400)
      except User.DoesNotExist:
        try:
          u = User.create(username=self.username, password_hash=elf.password, email=self.email)
          self.write(json_encode("successful"));
        except IntegrityError:
          params['error_username'] = "That user already exists."
          self.write(json_encode(params))
          self.set_status(400)
          
    self.set_header("Content-Type", "application/json") 
