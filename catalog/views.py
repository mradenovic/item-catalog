from catalog import app
from db import session
from flask import render_template, url_for, request, redirect, jsonify
from flask import session as login_session
from flask import flash
from db_setup import Category, Item, User
from auth import authenticate, authorize
from auth import get_user_id


categories = session.query(Category).order_by(Category.name.desc())

@app.route('/')
@app.route('/catalog')
def catalog():
    items = session.query(Item).order_by(Item.created_at.desc()).limit(10)
    return render_template('catalog.html', categories=categories, items=items, items_title='Latest')


@app.route('/catalog.json')
def catalog_jsonified():
    return jsonify(Category=[i.serialize for i in categories])


@app.route('/catalog/item/<int:item_id>/json')
def item_jsonfied(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


@app.route('/catalog/category/<int:category_id>/json')
def category_jsonfied(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(Category=category.serialize)


@app.route('/catalog/category/<int:category_id>')
def category_view(category_id):
    items = session.query(Item).filter_by(category_id=category_id).order_by(Item.name)
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('catalog.html', categories=categories, items=items, items_title=category.name)


@app.route('/catalog/item/new', methods=['GET', 'POST'])
@authenticate
def item_new():
    if request.method == 'POST':
        return item_new_post()
    else:
        return item_new_get()

def item_new_get():
    params = {}
    params['categories'] = categories
    params['item'] = None
    params['action'] = 'New'
    params['cancel_url'] = url_for('catalog')
    return render_template('itemForm.html', **params)

def item_new_post():
    params = {}
    params['name'] = request.form['name']
    params['description'] = request.form['description']
    params['price'] = request.form['price']
    params['category_id'] = request.form['category_id']
    params['user_id'] = get_user_id(login_session)
    item = Item(**params)
    session.add(item)
    session.commit()
    flash('New Item <strong>%s</strong> Successfully Created!' % (item.name), 'success')
    return redirect(url_for('item_view', item_id=item.id))

@app.route('/catalog/item/<int:item_id>')
def item_view(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('itemView.html', item=item)


@app.route('/catalog/item/<int:item_id>/edit', methods=['GET', 'POST'])
@authenticate
@authorize
def item_edit(item_id):
    if request.method == 'POST':
        return item_edit_post(item_id)
    else:
        return item_edit_get(item_id)

def item_edit_get(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    params = {}
    params['categories'] = categories
    params['item'] = item
    params['action'] = 'Edit'
    params['cancel_url'] = url_for('item_view', item_id=item_id)
    return render_template('itemForm.html', **params)

def item_edit_post(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    item.name = request.form['name']
    item.description = request.form['description']
    item.price = request.form['price']
    item.category_id = request.form['category_id']
    session.add(item)
    session.commit()
    flash('Item <strong>%s</strong> Successfully Updated!' % (item.name), 'success')
    return redirect(url_for('item_view', item_id=item.id))


@app.route('/catalog/item/<int:item_id>/delete', methods=['GET', 'POST'])
@authenticate
@authorize
def item_delete(item_id):
    if request.method == 'POST':
        return item_delete_post(item_id)
    else:
        return item_delete_get(item_id)

def item_delete_get(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    flash('<strong>Danger!</strong> This action can not be reverted!', 'danger')
    return render_template('itemView.html', item=item, delete=True)

def item_delete_post(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    session.delete(item)
    session.commit()
    flash('Item <strong>%s</strong> Successfully Deleted'% item.name, 'success')
    return redirect('catalog')
