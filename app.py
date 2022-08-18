#!/usr/bin/env python3
import os
from flask import Flask, request, flash, redirect, url_for, render_template
from flask_login import LoginManager, current_user
from database.engine import Transaction, Agent, DB
from database import storage
from forms import RegisterForm, LoginForm
from werkzeug.security import check_password_hash


SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_user = LoginManager(app)
login_user.login_view = 'login'
login_user.login_message = 'Please Login as Agent to continue'

app.url_map.strict_slashes = False

@login_user.user_loader
def find_user(agent):
    """Locate agent by id"""
    from database import storage
    return storage.get_agent_by_id(agent)

def logged_in(current_user: int) -> bool:
    """returns True if user is logged in"""
    try:
        _ = current_user.id
        return True
    except:
        return False

@app.route("/")
def index():
    db = DB()
    return ("My Name is Micheal Scoot")

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        agent = Agent(
            agent_no=form.agent_no.data,
            agent_name=form.agent_name.data,
            api_key=form.api_key.data,
            password=form.password.data,
            )
        storage.save(agent)
        # login_user(agent)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    uin = logged_in(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        agent = storage.get_agent_by_no(form.agent_no.data)
        print(agent)
        if agent and check_password_hash(agent.password, form.password.data):
            print("INNNNNNNNNNNNN")
            # login_user(agent)
            return redirect(url_for('index'))
        else:
            flash('Invalid Agent Number or Password', 'danger')
    return render_template('login.html', form=form)

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 33507))
    app.run(host="0.0.0.0", port=5000, debug=True)