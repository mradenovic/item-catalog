from catalog import app
from db import session
from flask import render_template
from db_setup import Category, Item, User


@app.route('/')
@app.route('/catalog')
def catalog():
    categories = session.query(Category).order_by(Category.name.desc())
    items = session.query(Item).order_by(Item.created_at).limit(10)
    return render_template('catalog.html', categories=categories, items=items)
