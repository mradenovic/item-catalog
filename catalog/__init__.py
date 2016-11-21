'''Create and configure Flask app'''

from flask import Flask
import config

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['GOOGLE_ID'] = config.GOOGLE_LOGIN_CLIENT_ID
app.config['GOOGLE_SECRET'] = config.GOOGLE_LOGIN_CLIENT_SECRET
app.debug = True


import views
import auth
