from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(80), unique=True)

    def __repr__(self):
        return f"\nname: {self.username}, id: {self.id}, email: {self.email}"


# TODO: make it derived from a common class EventBase()
class HeroRealmEvent(Base):
    __tablename__ = 'hero_realm_event'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    description = Column(String(250))
    user1_id = Column(Integer, ForeignKey(User.id))
    user1 = relationship(User, foreign_keys=[user1_id])
    user2_id = Column(Integer, ForeignKey(User.id))
    user2 = relationship(User, foreign_keys=[user2_id])

    def __repr__(self):
        return f"\nname: {self.name}, id: {self.id}"


engine = create_engine('sqlite:///boardgamehelper.db')
Base.metadata.create_all(engine)


