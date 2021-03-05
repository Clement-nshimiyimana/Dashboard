import dash
import dash_bootstrap_components as dbc
from flask import Flask, send_from_directory
from flask_caching import Cache
import os

from flask_login import LoginManager, UserMixin
from users_mgt import db, User as base
from config import config

## To assign session Id
import uuid

## get session ID
def get_session_id():
    return str(uuid.uuid4())
session_id = get_session_id()

server = Flask("My app")

# Dashboard deployment
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    server=server,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'I&M dashboard',
            'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
        }
    ]
)
app.title = "I&M Bank dashboard"


#################################################################################################
app.config.suppress_callback_exceptions = True 
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
# config
server.config.update(
    SECRET_KEY=os.urandom(15),
    SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db.init_app(app.server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# Create User class with UserMixin
class User(UserMixin, base):
    pass

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

############################ Cache and Session settings #####################################

TIMEOUT = 3600*24 ## In seconds 

CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',

    'CACHE_THRESHOLD': 200
}
cache1 = Cache()
cache1.init_app(app.server, config=CACHE_CONFIG)




