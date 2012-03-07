from sqlalchemy import Column
from sqlalchemy.types import UnicodeText
from sqlalchemy.types import Integer
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from datetime import datetime

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

class Chat(Base):
    __table_args__ = {'sqlite_autoincrement': True}
    __tablename__ = 'chat'

    pk =  Column(Integer, primary_key=True, autoincrement=True)
    chat_line = Column(UnicodeText, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)

def includeme(config):
    config.scan('chatter2.models')
