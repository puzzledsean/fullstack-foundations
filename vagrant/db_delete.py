from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# initialize a session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()

session.delete(spinach)
session.commit()
