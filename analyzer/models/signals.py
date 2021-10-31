from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

Base = declarative_base()
engine = create_engine('sqlite:///signals.db', echo=False, connect_args={'check_same_thread': False}, poolclass=StaticPool)
Session = sessionmaker(bind=engine)
db = Session()


class Signals(Base):

    __tablename__ = 'signals'
    id = Column(Integer, primary_key=True)
    pair = Column(String(30))
    price = Column(String(30))
    signal = Column(Integer())
    direction = Column(String(30))

    @staticmethod
    def get_or_create(pair):
        setup = db.query(Signals).filter_by(pair=pair).first()
        if setup is None:
            entry = Signals(pair=pair)
            db.add(entry)
            db.commit()
        setup = db.query(Signals).filter_by(pair=pair).first()
        return setup

    @staticmethod
    def find(pair):
        setup = Session().query(Signals).filter_by(pair=pair).first()
        return setup


Base.metadata.create_all(engine)
