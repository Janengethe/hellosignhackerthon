import os
from flask import Flask, request, flash, redirect, url_for, render_template
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Agent, Transaction

import helper_methods
from forms import TrnsctnForm, LoginForm, RegisterForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Please, Login to continue'


@login_manager.user_loader
def load_user(agent_id):
    """Locate user by id"""
    return Agent.query.get(int(agent_id))
    
app.url_map.strict_slashes = False


@app.route('/')
def index():
    uin = helper_methods.logged_in(current_user)
    return render_template("index.html", uin=uin)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    uin=helper_methods.logged_in(current_user)
    form = TrnsctnForm()
    if form.validate_on_submit():
        obj = Transaction(
            national_id=form.national_id.data,
            txn_type=form.txn_type.data,
            value=form.value.data,
            txn_id=form.txn_id.data)

        if current_user.is_authenticated:
            print(current_user)
            setattr(obj, 'agent_id', current_user.id)
            db.session.add(obj)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash("Please login first!")
            return redirect(url_for("login"))
    return render_template('dashboard.html', uin=uin, form=form)

@app.route('/transactions_list', methods=['GET', 'POST'])
@login_required
def transactions_list():
    uin = helper_methods.logged_in(current_user)
    agent_id = current_user.id
    trans = Transaction.query.filter_by(agent_id).first()
    return render_template("tlist.html", uin=uin, trans=trans)


@app.route('/register', methods=['GET', 'POST'])
def register():
    uin = helper_methods.logged_in(current_user)
    form = RegisterForm()
    if form.validate_on_submit():
        agent = Agent(
            agent_no=form.agent_no.data,
            agent_name=form.agent_name.data,
            email=form.email.data,
            password=form.password.data,
            )
        
        db.session.add(agent)
        db.session.commit()
        # hsgn = helper_methods.confi_g(agent.email)
        flash("A warm welcome. Check Email to confirm Signing!", "success")
        login_user(agent)
        return redirect(url_for('index'))
    return render_template('register.html', uin=uin, form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    uin = helper_methods.logged_in(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        agent = Agent.query.filter_by(agent_no=form.agent_no.data).first()
        if agent and check_password_hash(agent.password, form.password.data):
            login_user(agent)
            flash("Welcome")
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Agent Number or Password', 'danger')
    return render_template('login.html', uin=uin, form=form)

@app.route('/logout', methods=['GET'])
def logout():
    """return home page in response to logout"""
    logout_user()
    flash("See you later!", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
