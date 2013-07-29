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
from models import Category
from pprint import pprint

class CategoryHandler(BaseHandler):
  @classmethod
  def install(cls, handlers):
    handlers.append((r"/categories", CategoryHandler))
 
  @login_required 
  def get(self):
    categories = Category.select().order_by(Category.name).iterator()
    categoryList = [{'id': category.id, 'name': category.name} for category in categories]
    self.write(json_encode(categoryList))
    self.set_header("Content-Type", "application/json")
