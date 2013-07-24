import tornado.web
import logging
import functools
import json
import hashlib
from models import User

def login_required(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper

def make_salt(length = 10):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
      if self.request.headers.get("Content-Type") == "application/json":
        self.json_args = json.loads(self.request.body)
    
    def check_xsrf_cookie(self):
      return True

    def get_current_user(self):
      user_id = self.get_secure_cookie('user_id')
      if user_id is not None:
        logging.info("user_id: " + user_id)
        return User.get(User.id == user_id)
      else:
        logging.info("user id" + user_id + " not found")

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.id))

    def logout(self):
        self.clear_cookie('user_id')