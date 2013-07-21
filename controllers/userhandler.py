import tornado.web
from apiclient.discovery import build

import os
import sys
import httplib2
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from pycket.session import SessionMixin
from basehandler import *

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
print path
if not path in sys.path:
    sys.path.insert(1, path)

from models import User 

import json
import random
import string
import sys
import datetime
import logging

CLIENT_ID = json.loads(
    open('/home/ubuntu/app/app/client_secrets.json', 'r').read())['web']['client_id']
SERVICE = build('plus', 'v1')
PROVIDER = "Google"

class UserHandler(BaseHandler, SessionMixin):
  @classmethod
  def install(cls, handlers):
    handlers.append((r"/user/?(.*)", UserHandler))

  def check_xsrf_cookie(self):
    return True
  
  def mksession(self):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for x in xrange(32))

  def post(self, path):
    if path == 'connect':
      try:
        state_arg = self.get_argument("state")
        state_cookie = self.session.get("state")
        if state_arg != state_cookie:
          self.set_status(401)
          self.write(json.dumps({"msg:" : "Invalid state parameter", "state_arg" : state_arg, "state_cookie" : state_cookie})) 
          return      

        code = self.request.body	
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('/home/ubuntu/app/app/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
      except FlowExchangeError:
        self.set_status(401)
        self.write(
            json.dumps({"msg": 'Failed to upgrade the authorization code.'}))
        return
      
      gplus_id = credentials.id_token['sub']
      
      try:
        # use the .get() method to quickly see if a user with that name exists
        user = User.get(identifier=gplus_id,provider=PROVIDER)
        logging.info(user.identifier + " joined " + user.join_date.isoformat())
      except User.DoesNotExist:
        # if not, create the user and store the form data on the new model
        user = User.create(
                identifier=gplus_id,
                provider=PROVIDER,
                join_date=datetime.datetime.now()
        )
        logging.info(gplus_id + " just joined!")
 
      stored_credentials = self.session.get("credentials")
      stored_gplus_id = self.session.get('gplus_id')
      if stored_credentials is not None and gplus_id == stored_gplus_id:
        self.set_status(200)
        self.write(json.dumps({"msg": 'Current user is already connected.'}))
        return

      
      # Store the access token in the session for later use.
      self.session.set('credentials', credentials)
      self.session.set('gplus_id', gplus_id)
      self.write(json.dumps({"msg": 'Successfully connected user.'}))

  def get(self, path):
    if path == "people":
      self.people()

  @login_required
  def people(self):
    """Get list of people user has shared with this app."""
    credentials = self.session.get('credentials')
    # Only fetch a list of people for connected users.
    if credentials is None:
      self.write(json.dumps({"msg": 'Current user is not connected'}))
      self.set_status(401)
      return
   
    try:
      # Create a new authorized API client.
      http = httplib2.Http()
      http = credentials.authorize(http)
      # Get a list of people that this user has shared with this app.
      google_request = SERVICE.people().list(userId='me', collection='visible')
      result = google_request.execute(http=http)
      self.write(json.dumps(result))
      self.set_header("Content-Type", "application/json")
      return
    except AccessTokenRefreshError:
      self.write(json.dumps({"msg": 'Failed to refresh access token'}))
      self.set_status(500)
