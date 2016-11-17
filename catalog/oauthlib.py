from catalog import app
import config

from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
from db import session as db
from db_setup import User, Item
from functools import wraps


# app = Flask(__name__)
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


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
    user = User(name=session['username']['name'], email=session['user'][
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
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            session['next'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        item_id = kwargs['item_id']
        item = db.query(Item).filter_by(id=item_id).one()
        user_id = get_user_id(session)
        if item.user_id != user_id:
            return 'Not owner'
        return f(*args, **kwargs)
    return decorated_function
