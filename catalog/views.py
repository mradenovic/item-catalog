from catalog import app
from db import session
from flask import render_template
from db_setup import Category, Item, User


categories = session.query(Category).order_by(Category.name.desc())

@app.route('/')
@app.route('/catalog')
def catalog():
    items = session.query(Item).order_by(Item.created_at).limit(10)
    return render_template('catalog.html', categories=categories, items=items)


@app.route('/catalog.json')
def catalog_jsonified():
    return 'catalog jsonified'


@app.route('/catalog/category/<int:category_id>')
def category_view(category_id):
    items = session.query(Item).filter_by(category_id=category_id).order_by(Item.name)
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('catalog.html', categories=categories, items=items, items_title=category.name)


@app.route('/catalog/item/new')
def item_new():
    return 'new item'


@app.route('/catalog/item/<int:item_id>')
def item_view(item_id):
    return 'view %s' % item_id


@app.route('/catalog/item/<int:item_id>/edit')
def item_edit(item_id):
    return 'edit item %s' % item_id


@app.route('/catalog/item/<int:item_id>/delete')
def item_delete(item_id):
    return 'delete %s' % item_id
