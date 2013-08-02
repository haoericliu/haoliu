from libs.app_globals import g
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import Column
from sqlalchemy.sql import and_
from sqlalchemy.types import String, Integer

ENGINE_NAME = 'swapmeetdb'
ENGINE = g.dbm.get_engine(ENGINE_NAME)
Session = scoped_session(sessionmaker(bind=ENGINE))
Base = declarative_base(bind=ENGINE)

class Test(Base):
     __tablename__ = 'test'

     id = Column(Integer, primary_key=True)
     name = Column(String(50))
     fullname = Column(String(50))
     password = Column(String(12))

     def __init__(self, name, fullname, password):
         self.name = name
         self.fullname = fullname
         self.password = password

     def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

Base.metadata.create_all(ENGINE) 
print "MODEL 2 HELLO WORLD"