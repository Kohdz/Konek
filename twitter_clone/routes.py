from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime
from twitter_clone.models import User, Tweet, followers
from twitter_clone.forms import RegisterForm, LoginForm, TweetForm,UpdateAccountForm
from twitter_clone import app, login_manager, photos, db
import secrets, os
from PIL import Image


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html', title='Homepage')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        new_user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data), join_date=datetime.now())

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        
        # flash message that user has been created
        flash('User has been succesfully created! Please log in!', 'success')
        
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form, title="Register")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        # if username in database & pw correct
        # log the user in & flash success message
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been successfully logged in', 'success')
            return redirect(url_for('profile'))

        # if user does not exist - make the user retry their credentials
        if not user:
            flash('Login Failed. Please check your credentials and try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form, title='Log In')


# logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# save picture function
# NOTE: we will modify the filename of the uploaded image so there won't be confusion in our database if different filenames of the same image is uploaded
def save_picture(image):
    random_hex = secrets.token_hex(8)
    # split image filename
    _, f_ext = os.path.splitext(image.filename)
    # create modified name for picture file
    picture_name = random_hex + f_ext
    # create absolute path for new picture image
    picture_path = os.path.join(app.root_path, 'static/imgs', picture_name)
    # save the image to the picture_path we created
    image.save(picture_path)

    # resize image upload with PIL
    output_size = (125, 125)
    i = Image.open(image)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name


# update user account info route
@app.route('/account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            # set current user's image
            current_user.image = picture_file

        # update our current username and email
        current_user.username = form.username.data
        current_user.email = form.email.data
        # make changes to our database
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('update_account'))
    
    # prepopulate the form fields with current user's info
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='imgs/' + current_user.image)

    return render_template('update_account.html', title='Update Account', form=form, image_file=image_file)


@app.route('/profile', defaults={'username': None})
@app.route('/profile/<username>')
def profile(username):

    image_file = url_for('static', filename='imgs/' + current_user.image)

    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
    else:
        user = current_user

    tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).all()
    current_time = datetime.now()
    followed_by = user.followed_by.all()

    display_follow = True

    liked_by= user.liked_by.all()

    if current_user == user:
        display_follow = False
    else:
        if current_user in followed_by:
            display_follow = False


    return render_template('profile.html', title='Profile', current_user=user, tweets=tweets,
         current_time=current_time, followed_by=followed_by, image_file=image_file,
             display_follow=display_follow, liked_by=liked_by)


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
    
        tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).all()
        total_tweets = len(tweets)

    else:
        user = current_user
        tweets = Tweet.query.join(followers, (followers.c.following_id == Tweet.user_id)).filter(followers.c.follower_id == current_user.id).order_by(Tweet.date_created.desc()).all()
        total_tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).count()
    

    current_time = datetime.now()

    followed_by_count = user.followed_by.count()
    liked_by_count = user.liked_by.count()

    who_to_watch = User.query.filter(User.id != user.id).order_by(db.func.random()).limit(4).all()

    return render_template('timeline.html', title="Timeline", form=form, tweets=tweets,
         current_time=current_time, current_user=user, total_tweets=total_tweets, who_to_watch=who_to_watch,
         followed_by_count=followed_by_count, liked_by_count=liked_by_count)


@app.route('/post_tweet', methods=['POST'])
@login_required
def post_tweet():
    form = TweetForm()

    if form.validate():

        tweet = Tweet(user_id=current_user.id, text=form.text.data, date_created=datetime.now())
        db.session.add(tweet)
        db.session.commit()


        return redirect(url_for('timeline'))

    flash('Something Went Wrong/Form Not Valid', 'danger')


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


@app.route('/follow/<username>')
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()

    current_user.following.append(user_to_follow)

    db.session.commit()
    
    return redirect(url_for('profile'))


# give  a tweet a like paramater
#then make a url where the like goes by a count of 1
# @app.route('/like/<tweet>')



        
