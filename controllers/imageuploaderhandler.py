import tornado.web

from pprint import pprint
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

import os
import sys

from basehandler import *

import json
import sys
import datetime
import logging
from tornado.escape import json_encode
from models import User
from models import Photo
from models import Item
import base64
from models import Models2

class ImageUploaderHandler(BaseHandler):
  @classmethod
  def install(cls, handlers):
    handlers.append((r"/upload", ImageUploaderHandler))
  
  @login_required
  def post(self):
    image = self.request.files['file'][0]
    imagebody = image['body']
    imagename = image['filename']
    imagetype = image['content_type']

    item = Item.create(user=self.current_user, created_date=datetime.datetime.now())
    newImageName = base64.b32encode(str(item.id)) # use item id as the randomly generated file name
    conn = boto.connect_s3()
    bucket = conn.get_bucket('i.haoliu.net')
    key = Key(bucket)
    key.key = newImageName
    key.set_metadata("Content-Type", imagetype)
    key.set_contents_from_string(imagebody)
    key.set_acl('public-read')
    self.write(newImageName + " " + imagetype + " " + str(len(imagebody)))
    photo = Photo.create(identifier=newImageName, item=item) 
     
    imgLoc = 'http://i.haoliu.net/' + newImageName;
    self.write(json_encode(imgLoc))
    self.set_header("Content-Type", "application/json") 


    
    
    
