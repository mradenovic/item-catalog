'''Create and configure Flask app'''

from flask import Flask

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.debug = True


import views
import auth
