from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, HeroRealmEvent

engine = create_engine('sqlite:///boardgamehelper.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

session.query(User).delete()
session.query(HeroRealmEvent).delete()
session.commit()

myFirstPlayer = User(username='Rémi Piquette')
session.add(myFirstPlayer)

mySecondPlayer = User(username='Patrick Piquette',
                      email="ppiquette@yahoo.com")
session.add(mySecondPlayer)

game1 = HeroRealmEvent(name='Cheese Pizza Game',
                       description='The return of Rémi',
                       user1=myFirstPlayer,
                       user2=mySecondPlayer)
session.add(game1)
session.commit()

print(session.query(User).all())
print(session.query(HeroRealmEvent).all())
