import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3ConnectionHelper(object):
  _boto_connection = None
  _bucket = None  

  def __init__(self):
    '''Make these configurable'''
    self._boto_connection = boto.connect_s3()
    self._bucket = self._boto_connection.get_bucket('i.haoliu.net')

  def uploadPublicImageFromString(self, s3KeyName, imageString):
    key = Key(self._bucket)
    key.key = s3KeyName
          # todo: check content-type 
    key.set_metadata("Content-Type", "image/jpeg")
    key.set_contents_from_string(imageString)
    key.set_acl('public-read')