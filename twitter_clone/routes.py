from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime
from twitter_clone.models import User, Tweet
from twitter_clone.forms import RegisterForm, LoginForm, TweetForm
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        image_filename = photos.save(form.image.data)
        image_url = photos.url(image_filename)

        new_user = User(name=form.name.data, username=form.username.data, email=form.email.data, image=image_url, password=generate_password_hash(form.password.data), join_date=datetime.now())

        db.session.add(new_user)
        db.session.commit()
        
        # flash message that user has been created
        flash('User has been succesfully created! Please log in!')
        
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form, title="Register")


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


@app.route('/profile', defaults={'username': None})
@app.route('/profile/<username>')
def profile(username):

    if username:
        user = User.query.filter_by(username=username).first()
        
        if not user:
            abort(404)
    else:
        user = current_user

    tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).all()

    current_time = datetime.now()

    return render_template('profile.html', title="Profile", current_user=user, tweets=tweets, current_time=current_time)


# needs a login required route (commented until no more dummy data)
# @login_required
@app.route('/timeline', defaults={'username': None})
@app.route('/timeline/<username>')
def timeline(username):
    form = TweetForm()

    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
    
    else:
        user = current_user

    
    tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).all()

    total_tweets = len(tweets)

    current_time = datetime.now()

    return render_template('timeline.html', title="Timeline", form=form, tweets=tweets, current_time=current_time, current_user=user, total_tweets=total_tweets)

@app.route('/post_tweet', methods=['POST'])
@login_required
def post_tweet():
    form = TweetForm()

    if form.validate():

        tweet = Tweet(user_id=current_user.id, text=form.text.data, date_created=datetime.now())
        db.session.add(tweet)
        db.session.commit()


        return redirect(url_for('timeline'))

    return 'Something Went Wrong/Form Not Valid'

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






        
