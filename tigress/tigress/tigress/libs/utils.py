import re
import random
from string import letters
import hashlib
import functools
from tigress.libs.errors import UnauthorizedError

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
  return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
  return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
  return not email or EMAIL_RE.match(email)

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

def login_required(method):
  """Decorate methods with this to require that the user be logged in.

  If the user is not logged in, they will be redirected to the configured
  `login url <RequestHandler.get_login_url>`.
  """
  @functools.wraps(method)
  def wrapper(self, *args, **kwargs):
    if not self.user:
      raise UnauthorizedError("Not logged in")
    return method(self, *args, **kwargs)
  return wrapper