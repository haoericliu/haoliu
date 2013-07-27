from peewee import *

DATABASE_HOST = 'mysql-alpha.cjpncjgbwi8i.us-west-2.rds.amazonaws.com'

# create a peewee database instance -- our models will use this database to
# persist information
database = MySQLDatabase("mydb", host=DATABASE_HOST, port=3306, user="helios", passwd="BM33Bo5dnhkKz5jvuVx")

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

class Photo(BaseModel):
    identifier = CharField(unique=True)
    location = CharField()

def create_tables():
    database.connect()
    User.create_table(True)
    Photo.create_table(True)
    
if __name__ == "__main__":
    create_tables()
