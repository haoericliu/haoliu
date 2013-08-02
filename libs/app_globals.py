from datetime import datetime
from sqlalchemy import engine, event
import db_manager
from pprint import pprint


class Globals(object):

  def setup(self):
    self.dbm = self.load_db_params()

  def load_db_params(self):
    dbm = db_manager.db_manager()
    pprint(dir(dbm))
    dbm.setup_db(db_name='swapmeetdb', db_user='swapmeet', db_pass='9TsHg5sus6fcvciXKPLM', db_host='mysql.haoliu.net')
    return dbm

g = Globals()
g.setup()
print "Global 1111"