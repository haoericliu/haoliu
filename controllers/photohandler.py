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

class PhotoHandler(BaseHandler):
  @classmethod
  def install(cls, handlers):
    handlers.append((r"/photos", PhotoHandler))
  
  def get(self):
    photos = Photo.select().iterator()
    photoList = [{'id': photo.id, 'identifier': photo.identifier} for photo in photos]
    self.write(json_encode(photoList))
    self.set_header("Content-Type", "application/json")
