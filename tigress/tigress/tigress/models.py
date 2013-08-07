from mongoengine import *
import datetime

class User(DynamicDocument):
  username = StringField(max_length=50, required=True, unique=True)
  password_hash = StringField(required=True)
  email = EmailField(unique=True, required=True)
  join_date = DateTimeField(default=datetime.datetime.now)

  def __json__(self, request):
    return {'username' : self.username, 'email' : self.email}

class Item(DynamicDocument):
  description = StringField(max_length=200)
  creation_date = DateTimeField(default=datetime.datetime.now)
  tags = ListField(StringField(max_length=50))

  def __json__(self, request):
    return {'description' : self.description, 'tags' : tags}
