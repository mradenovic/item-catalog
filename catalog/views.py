from catalog import app
from db import session
from flask import render_template, url_for, request, redirect
from db_setup import Category, Item, User


categories = session.query(Category).order_by(Category.name.desc())

@app.route('/')
@app.route('/catalog')
def catalog():
    items = session.query(Item).order_by(Item.created_at).limit(10)
    return render_template('catalog.html', categories=categories, items=items, items_title='Latest')


@app.route('/catalog.json')
def catalog_jsonified():
    return 'catalog jsonified'


@app.route('/catalog/category/<int:category_id>')
def category_view(category_id):
    items = session.query(Item).filter_by(category_id=category_id).order_by(Item.name)
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('catalog.html', categories=categories, items=items, items_title=category.name)


@app.route('/catalog/item/new', methods=['GET', 'POST'])
def item_new():
    if request.method == 'POST':
        params = {}
        params['name'] = request.form['name']
        params['description'] = request.form['description']
        params['price'] = request.form['price']
        params['category_id'] = request.form['category_id']
        item = Item(**params)
        session.add(item)
        session.commit()
        # flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('item_view', item_id=item.id))
    else:
        params = {}
        params['categories'] = categories
        params['item'] = None
        params['action'] = 'New'
        params['cancel_url'] = url_for('catalog')
        return render_template('itemForm.html', **params)


@app.route('/catalog/item/<int:item_id>')
def item_view(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('itemView.html', item=item)


@app.route('/catalog/item/<int:item_id>/edit')
def item_edit(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    params = {}
    params['categories'] = categories
    params['item'] = item
    params['action'] = 'Edit'
    params['cancel_url'] = url_for('item_view', item_id=item_id)
    return render_template('itemForm.html', **params)


@app.route('/catalog/item/<int:item_id>/delete')
def item_delete(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('itemView.html', item=item, delete=True)
