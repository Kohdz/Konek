from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

from twitter_clone.models import User
from twitter_clone.forms import RegisterForm, LoginForm
from twitter_clone import app, login_manager, photos, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():

    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>Username: {}, Password: {}, Remember: {}</h1>'.format(form.username.data, form.password.data, form.remember.data)

    return render_template('index.html', form=form, title="Homepage")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            return 'Login Failed'

        if check_password_hash(user.password, form.password.data):
            login_user(user)

            return redirect(url_for('profile'))

        return 'Login failed'
    
    return redirect(url_for('index'))


# logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# needs a login required route (commented out until no more dummy data)
# @login_required
@app.route('/profile')
def profile():
    return render_template('profile.html', title="Profile")


# needs a login required route (commented until no more dummy data)
# @login_required
@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        image_filename = photos.save(form.image.data)
        image_url = photos.url(image_filename)

        new_user = User(name=form.name.data, username=form.username.data, image=image_url, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('profile'))
    
    return render_template('register.html', form=form, title="Register")