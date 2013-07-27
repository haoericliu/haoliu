import tornado.web
from apiclient.discovery import build
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
from models import Photo

class ImageUploaderHandler(BaseHandler):
  @classmethod
  def install(cls, handlers):
    handlers.append((r"/upload", ImageUploaderHandler))
  
  def post(self):
    image = self.request.files['file'][0]
    imagebody = image['body']
    imagename = image['filename']
    imagetype = image['content_type']
    self.write(imagename + " " + imagetype + " " + str(len(imagebody)))
    conn = boto.connect_s3()
    bucket = conn.get_bucket('imgur.haoliu.net')
    key = Key(bucket)
    key.key = imagename
    key.set_metadata("Content-Type", imagetype)
    key.set_contents_from_string(imagebody)
    key.set_acl('public-read')
    self.write(imagename + " " + imagetype + " " + str(len(imagebody)))
