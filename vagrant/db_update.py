from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# initialize a session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

veggie_burgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')


urban_veggie_burger = session.query(MenuItem).filter_by(id=9).one()
urban_veggie_burger.price = '$2.99'
session.add(urban_veggie_burger)
session.commit()

for veggie_burger in veggie_burgers:
    if veggie_burger.price != '$2.99':
        veggie_burger.price = '$2.99'
        session.add(veggie_burger)
        session.commit()

for veggie_burger in veggie_burgers:
    print(veggie_burger.id)
    print(veggie_burger.price)
    print(veggie_burger.restaurant.name)
    print()
