from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash
from konek.search.forms import SearchForm
from konek.users.forms import RegisterForm
from konek.models import User
from konek import db, login_manager, app
from datetime import datetime


main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.template_filter('time_passed')
def time_passed(seconds_since):

    seconds = seconds_since.total_seconds()
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days > 0:
        return '%dd' % (days)
    elif hours > 0:
        return '%dh' % (hours)
    elif minutes > 0:
        return '%dm' % (minutes)
    else:
        return 'now'


@main.route('/')
def index():
    form = SearchForm()
    return render_template('index.html', title='Homepage', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        new_user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data), join_date=datetime.now())

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        
        # flash message that user has been created
        flash('User has been succesfully created! Please log in!', 'success')
        
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form, title="Register")