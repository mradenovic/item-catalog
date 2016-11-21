'''Authentication and authorization

This module contains all authentication and authorization methods.

'''

from catalog import app
from config import GOOGLE

from flask import Flask, redirect, url_for, session, request, jsonify
from flask import flash
from flask_oauthlib.client import OAuth
from db import session as db
from db_setup import User, Item
from functools import wraps


# app = Flask(__name__)
oauth = OAuth(app)

google = oauth.remote_app('google', **GOOGLE)


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('user', None)
    session.pop('next', None)
    return redirect(url_for('catalog'))


@app.route('/login/authorized')
def authorized():
    '''Callback function to be executed after authentication with google'''

    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    session['user'] = google.get('userinfo').data

    user_id = get_user_id(session)
    if 'next' in session:
        next_url = session['next']
    else:
        next_url = None
    return redirect(next_url or url_for('catalog'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# User Helper Functions


def create_user(session):
    user = User(name=session['user']['name'], email=session['user'][
                   'email'], picture=session['user']['picture'])
    db.add(user)
    db.commit()
    user = db.query(User).filter_by(email=session['email']).one()
    return user.id


def get_user_id(session):
    try:
        email = session['user']['email']
        user = db.query(User).filter_by(email=email).one()
        return user.id
    except:
        try:
            user_id = create_user(session)
            return user_id
        except:
            return None

def authenticate(f):
    '''View decorator that authenticates user.

    User is authenticated if user is logged in.
    Args:
        f: Function to decorate.

    Returns:
        Decorated function if user is logged in, redirect to login if
        user is not logged in.

    '''

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            session['next'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def authorize(f):
    '''View decorator that authorizes user.

    User is authorized if user is owner of the item.
    Args:
        f: Function to decorate.

    Returns:
        Decorated function if user is athorized, redirect to item_view if
        user is not authorized.

    '''

    @wraps(f)
    def decorated_function(*args, **kwargs):
        item_id = kwargs['item_id']
        item = db.query(Item).filter_by(id=item_id).one()
        user_id = get_user_id(session)
        if item.user_id != user_id:
            flash('<strong>Warning!</strong> Only owner can perform this action!', 'warning')
            return redirect(url_for('item_view', item_id=item_id))
        return f(*args, **kwargs)
    return decorated_function
