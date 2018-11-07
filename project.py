from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
db = SQLAlchemy(app)
session = db.session

from database_setup import Restaurant, MenuItem


@app.route("/")
@app.route("/restaurants/<int:restaurant_id>/")
def restaurant_menu(restaurant_id=0):
    if restaurant_id != 0:
        restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
        menu_items = session.query(MenuItem).filter(MenuItem.restaurant == restaurant).all()
    return render_template('menu.html', restaurant=restaurant, items=menu_items)


@app.route("/restaurants/<int:restaurant_id>/new/", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['itemname'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New item created!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
    if request.method == 'POST':
        menu_item.name = request.form['newitemname']
        session.commit()
        flash("Item edited")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_item=menu_item)


@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete", methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
    if request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        flash("Item deleted")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=menu_item)

@app.route("/restaurants/<int:restaurant_id>/JSON")
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    menu_items = session.query(MenuItem).filter(MenuItem.restaurant == restaurant).all()
    return jsonify(MenuItems=[i.serialize for i in menu_items])

@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/JSON")
def restaurantMenuItemJSON(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
    return jsonify(MenuItems=[menu_item.serialize])


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

