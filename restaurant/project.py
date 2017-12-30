# lesson 3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
SESSION_KEY = os.getenv('SESSION_KEY')

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# JSON API endpoint
@app.route('/restaurants/JSON')
def listRestaurantsJSON():
    restaurants = session.query(Restaurant)
    return jsonify(Restaurant=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def listMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def listMenuItemJSON(restaurant_id, menu_id):
    requested_menuitem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItems=requested_menuitem.serialize)

# ---------------------------------------------------------------------------------
# Restaurant Logic
#   - Handle CRUD operations for restaurants
# ---------------------------------------------------------------------------------

# Show all restaurants
@app.route('/')
@app.route('/restaurants')
def listRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

# Create new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash('new restaurant created!')
        return redirect(url_for('listRestaurants'))
    else:
        return render_template('newrestaurant.html')

# Edit existing restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restauranttoedit = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restauranttoedit.name = request.form['name']
        session.add(restauranttoedit)
        session.commit()
        flash('restaurant name edited!')
        return redirect(url_for('listRestaurants', restaurant_id = restaurant_id))
    else:
        return render_template('editrestaurant.html', restaurant_id = restaurant_id, restaurant = restauranttoedit)

# Delete existing restaurant 
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restauranttodelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restauranttodelete)
        session.commit()
        flash('Restaurant deleted!')
        return redirect(url_for('listRestaurants', restaurant_id = restaurant_id))
    else:
        return render_template('deleterestaurant.html', restaurant_id = restaurant_id, restaurant = restauranttodelete)


# ---------------------------------------------------------------------------------
# Restaurant Menu Logic
#   - Handle CRUD operations for menu items at a given restaurant
# ---------------------------------------------------------------------------------

# Show all menu items at restaurant
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def listMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Create new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        item_name = request.form['name']
        item_description = request.form['description']
        item_price= request.form['price']
        item_course = request.form['course']

        newItem = MenuItem(name = item_name, description = item_description, price = item_price, course = item_course, restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash('new menu item created!')
        return redirect(url_for('listMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Edit exiting menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    itemtoedit = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        itemtoedit.name = request.form['name']
        session.add(itemtoedit)
        session.commit()
        flash('menu item edited!')
        return redirect(url_for('listMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = itemtoedit)

# Delete existing menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemtodelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemtodelete)
        session.commit()
        flash('menu item deleted!')
        return redirect(url_for('listMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = itemtodelete)

if __name__ == '__main__':
    app.secret_key = SESSION_KEY 
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
