from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sqlite3
import os


class db:
    def __init__(self, db_path):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            user = sqlite3.connect(self.db_path)
            user.close()

        engine = create_engine('sqlite:///{}'.format(db_path))
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))
        self.Base = declarative_base()
        self.Base.query = self.db_session.query_property()
        self.Base.metadata.create_all(bind=engine)






