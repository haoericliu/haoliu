import tornado.web
from pycket.session import SessionMixin
import logging
import functools
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

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
      gplus_id = self.session.get('gplus_id')
      if gplus_id is not None:
        logging.info("user id: " + gplus_id)
        return User.get(identifier=gplus_id,provider="Google")
      else:
        logging.info("user not found")
