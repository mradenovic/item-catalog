'''Flask app views.'''

from catalog import app
from db import session
from flask import render_template, url_for, request, redirect, jsonify
from flask import session as login_session
from flask import flash
from db_setup import Category, Item, User
from auth import authenticate, authorize
from auth import get_user_id
from validate import validate_record
from forms import ItemForm, flash_form_errors


categories = session.query(Category).order_by(Category.name.desc())
'''Imutable global category list'''

@app.route('/')
@app.route('/catalog')
def catalog():
    items = session.query(Item).order_by(Item.created_at.desc()).limit(10)
    return render_template('catalog.html', categories=categories, items=items, items_title='Latest')


@app.route('/catalog/json')
def catalog_jsonified():
    return jsonify(Category=[i.serialize for i in categories])


@app.route('/catalog/item/<int:item_id>/json')
@validate_record('Item')
def item_jsonfied(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


@app.route('/catalog/category/<int:category_id>/json')
@validate_record('Category')
def category_jsonfied(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(Category=category.serialize)


@app.route('/catalog/category/<int:category_id>')
@validate_record('Category')
def category_view(category_id):
    items = session.query(Item).filter_by(category_id=category_id).order_by(Item.name)
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('catalog.html', categories=categories, items=items, items_title=category.name)


@app.route('/catalog/item/new', methods=['GET', 'POST'])
@authenticate
def item_new():
    form = ItemForm(request.form)
    form.category_id.choices = [(cat.id, cat.name) for cat in categories]
    if request.method == 'POST' and form.validate():
        return item_new_post(form)
    else:
        return item_new_get(form)

def item_new_get(form):
    '''item_new GET handler'''

    params = {}
    params['form'] = form
    params['action'] = 'New'
    params['cancel_url'] = url_for('catalog')
    flash_form_errors(form)
    return render_template('itemEditForm.html', **params)

def item_new_post(form):
    '''item_new POST handler'''

    params = {}
    params['name'] = form.name.data
    params['description'] = form.description.data
    params['price'] = str(form.price.data)
    params['category_id'] = form.category_id.data
    params['user_id'] = get_user_id(login_session)
    item = Item(**params)
    session.add(item)
    session.commit()
    flash('New Item <strong>%s</strong> Successfully Created!' % (item.name), 'success')
    return redirect(url_for('item_view', item_id=item.id))

@app.route('/catalog/item/<int:item_id>')
@validate_record('Item')
def item_view(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('itemView.html', item=item)


@app.route('/catalog/item/<int:item_id>/edit', methods=['GET', 'POST'])
@validate_record('Item')
@authenticate
@authorize
def item_edit(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    item.price = float(item.price)
    form = ItemForm(request.form, item)
    form.category_id.choices = [(cat.id, cat.name) for cat in categories]
    if request.method == 'POST' and form.validate():
        return item_edit_post(form, item)
    else:
        return item_edit_get(form, item)

def item_edit_get(form, item):
    '''item_edit GET handler'''

    params = {}
    params['form'] = form
    params['action'] = 'Edit'
    params['cancel_url'] = url_for('item_view', item_id=item.id)
    flash_form_errors(form)
    return render_template('itemEditForm.html', **params)

def item_edit_post(form, item):
    '''item_edit POST handler'''

    item.name = form.name.data
    item.description = form.description.data
    item.price = str(form.price.data)
    item.category_id = form.category_id.data
    session.add(item)
    session.commit()
    flash('Item <strong>%s</strong> Successfully Updated!' % (item.name), 'success')
    return redirect(url_for('item_view', item_id=item.id))


@app.route('/catalog/item/<int:item_id>/delete', methods=['GET', 'POST'])
@validate_record('Item')
@authenticate
@authorize
def item_delete(item_id):
    if request.method == 'POST':
        return item_delete_post(item_id)
    else:
        return item_delete_get(item_id)

def item_delete_get(item_id):
    '''item_delete GET handler'''

    item = session.query(Item).filter_by(id=item_id).one()
    flash('<strong>Danger!</strong> This action can not be reverted!', 'danger')
    return render_template('itemView.html', item=item, delete=True)

def item_delete_post(item_id):
    '''item_delete POST handler'''

    item = session.query(Item).filter_by(id=item_id).one()
    session.delete(item)
    session.commit()
    flash('Item <strong>%s</strong> Successfully Deleted'% item.name, 'success')
    return redirect('catalog')
