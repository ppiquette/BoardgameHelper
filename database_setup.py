import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


class HeroRealmEvent(Base):
    __tablename__ = 'hero_realm_event'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    description = Column(String(250))
    user1_id = Column(Integer, ForeignKey(User.id))
    user1 = relationship(User)
    user2_id = Column(Integer, ForeignKey(User.id))
    user2 = relationship(User)

    def __repr__(self):
        return "Name: %s" % self.name

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id
        }


engine = create_engine('sqlite:///boardgamehelper.db')
Base.metadata.create_all(engine)


