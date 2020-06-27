from datetime import datetime
import json

from sqlalchemy import (
    DateTime,
    create_engine,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .models import Element, Type


engine = create_engine('sqlite:///.DS_Store', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class TypeDB(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    elements = Column(String(), default='{}')
    version = Column(Integer, default=0)
    updated = Column(DateTime, default=datetime.utcnow())

    def __init__(self, t: Type):
        self.name = t.name
        self.elements = json.dumps(t.elements)

    def to_type(self):
        return Type(
            name=self.name,
            elements=[Element(name=el['name'], type=el['type']) for el in json.loads(self.elements)],
            version=self.version,
            updated=self.updated,
        )


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)
