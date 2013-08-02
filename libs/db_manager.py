import logging
import os
import random
import socket
import sqlalchemy
import time
import traceback

logger = logging.getLogger('db_manager')
logger.addHandler(logging.StreamHandler())

def get_engine(db_name, db_host, db_user, db_pass, db_port='3306',
               pool_size=5, max_overflow=5):

  if db_name is None or db_host is None or db_user is None or db_pass is None:
    return

  #dialect+driver://username:password@host:port/database
  endpoint = "mysql://%s:%s@%s:%s/%s" % (db_user, db_pass, db_host, db_port, db_name)
  print endpoint 

  return sqlalchemy.create_engine(
    endpoint,
    strategy='threadlocal',
    pool_size=int(pool_size),
    max_overflow=int(max_overflow),
  )

class db_manager:
    def __init__(self):
        self._engines = {}
        self.dead = {}

    def setup_db(self, db_name, db_host, db_user, db_pass):
        engine = get_engine(db_name, db_host, db_user, db_pass)
        self._engines[db_name] = engine
        self.test_engine(engine)

    def mark_dead(self, engine):
        logger.error("db_manager: marking connection dead: %r", engine)
        self.dead[engine] = time.time()

    def test_engine(self, engine):
        try:
            list(engine.execute("select 1"))
            if engine in self.dead:
                logger.error("db_manager: marking connection alive: %r",
                             engine)
                del self.dead[engine]
            return True
        except Exception:
            logger.error(traceback.format_exc())
            logger.error("connection failure: %r" % engine)
            self.mark_dead(engine)
            return False

    def get_engine(self, name):
        return self._engines[name]

    def get_engines(self, names):
        return [self._engines[name] for name in names if name in self._engines]