#!/usr/bin/env python3
"""Module app"""
import os
from flask_login import LoginManager
from flask import Flask

from msahihi.database.engine import Agent


SECRET_KEY = os.urandom(32)

app = Flask(__name__)
default_database_path= "postgres:///database.db"
database_path = os.getenv('DATABASE_URL', default_database_path)
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = SECRET_KEY

login_user = LoginManager(app)
login_user.login_view = 'login'
login_user.login_message = 'Please, Login to continue'


@login_user.user_loader
def find_user(agent):
    """Locate user by id"""
    from msahihi.database import storage
    return storage.get_agent_by_id(agent)


from msahihi import routes