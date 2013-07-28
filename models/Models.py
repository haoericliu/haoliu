from peewee import *

DATABASE_HOST = 'mysql.haoliu.net'

# create a peewee database instance -- our models will use this database to
# persist information
database = MySQLDatabase("swapmeetdb", host=DATABASE_HOST, port=3306, user="swapmeet", passwd="9TsHg5sus6fcvciXKPLM")

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage. for more information, see:
# http://charlesleifer.com/docs/peewee/peewee/models.html#model-api-smells-like-django
class BaseModel(Model):
  class Meta:
    database = database

# the user model specifies its fields (or columns) declaratively, like django
class User(BaseModel):
  username = CharField(unique=True)
  password_hash = CharField()
  email = CharField()
  join_date = DateTimeField()

  class Meta:
    order_by = ('username',)

class Item(BaseModel):
  user = ForeignKeyField(User, related_name='items')
  created_date = DateTimeField()

class Photo(BaseModel):
  identifier = CharField(unique=True)
  item = ForeignKeyField(Item, related_name='photos')

def create_tables():
  database.connect()
  User.create_table(True)
  Photo.create_table(True)
  Item.create_table(True)
    
if __name__ == "__main__":
  create_tables()
