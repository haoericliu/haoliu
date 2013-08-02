import tornado.web

import os
import sys

from basehandler import *

import json
import sys
import datetime
import logging
from tornado.escape import json_encode
from models import Photo
from models import User
from models import Item
from pprint import pprint

class UserHandler(BaseHandler):
  @classmethod
  def install(cls, handlers):
    handlers.append((r"/photos/user", UserHandler))
 
  @login_required 
  def get(self):
    photos = self.current_user.items.photos
    photoList = [{'id': photo.id, 'identifier': photo.identifier} for photo in photos]
    #items = Item.select().where(Item.user == self.current_user)
    #photos = [item.photos for item in items]
    #photoList = []
    #for photo in photos:
    #  for i in photo:
    #    photoList.append({'id': i.id, 'identifier': i.identifier})
    self.write(json_encode(photoList))
    self.set_header("Content-Type", "application/json")
