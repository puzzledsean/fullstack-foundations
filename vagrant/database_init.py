from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# initialize a session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# add first restaurant
first_restaurant = Restaurant(name = 'Pizza Palace')
session.add(first_restaurant)
session.commit()

# add menu item
cheese_pizza = MenuItem(name = "Cheese Pizza", 
                        description = "Made with all natural ingredients and fresh mozzarella",
                        course = "Entree",
                        price = "$8.99",
                        restaurant = first_restaurant)
session.add(cheese_pizza)
session.commit()

print('successfully added pizza restaurant and cheese pizza onto menu')
