from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from konek.users.utils import save_picture
from konek.users.forms import RegisterForm, LoginForm, UpdateAccountForm
from konek.tweets.forms import TweetForm
from konek.models import User, Tweet, followers
from konek import db
from datetime import datetime
from sqlalchemy import or_


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data,
                        username=form.username.data,
                        email=form.email.data,
                        password=generate_password_hash(form.password.data),
                        join_date=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        flash('User has been succesfully created! Please log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title="Register")


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been successfully logged in', 'success')
            return redirect(url_for('users.profile'))
        if not user:
            flash('Login Failed. Please check your credentials and try again.',
                  'danger')
            return redirect(url_for('users.login'))
    return render_template('login.html', form=form, title='Log In')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            current_user.image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.update_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='imgs/' + current_user.image)
    return render_template('update_account.html',
                           title='Update Account',
                           form=form,
                           image_file=image_file)


@users.route('/profile', defaults={'username': None})
@users.route('/profile/<username>')
def profile(username):
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
    else:
        user = current_user
    image_file = url_for('static', filename='imgs/' + user.image)
    tweets = Tweet.query.filter_by(user=user).order_by(
        Tweet.date_created.desc()).all()
    current_time = datetime.now()
    followed_by = user.followed_by.all()
    followings = user.following.all()
    # breakpoint()
    if current_user == user:
        display_follow = False
        display_unfollow = False

    elif user in current_user.following:
        display_follow = False
        display_unfollow = True 
    else:
        display_follow = True
        display_unfollow = False
         
    # if not current_user and not display_follow
    return render_template('profile.html',
                           title='Profile',
                           current_user=user,
                           tweets=tweets,
                           current_time=current_time,
                           followed_by=followed_by,
                           image_file=image_file,
                           display_follow=display_follow,
                           display_unfollow=display_unfollow,
                           followings=followings)


@users.route('/timeline')
def timeline():
    image_file = url_for('static', filename='imgs/' + current_user.image)
    form = TweetForm()
    user = User.query.filter_by(username=current_user.username).first()
    if not user:
        abort(404)

    follower_query = db.session.query(followers.c.following_id).filter(followers.c.follower_id==user.id)
    tweets = db.session.query(Tweet).filter(or_(Tweet.user_id.in_(follower_query), Tweet.user_id==user.id)).order_by(Tweet.date_created.desc()).all()

    user_tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).all()
    total_tweets = len(user_tweets)
    current_time = datetime.now()
    followed_by_count = user.followed_by.count()
    who_to_watch = User.query.filter(User.id != user.id).order_by(
        db.func.random()).limit(4).all()
    return render_template('timeline.html',
                           title="Timeline",
                           form=form,
                           tweets=tweets,
                           current_time=current_time,
                           current_user=user,
                           total_tweets=total_tweets,
                           who_to_watch=who_to_watch,
                           followed_by_count=followed_by_count,
                           image_file=image_file)


@users.route('/follow/<username>')
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()
    if user_to_follow not in current_user.following:
        current_user.following.append(user_to_follow)
        db.session.commit()
    return redirect(url_for('users.profile', username=user_to_follow.username))


@users.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user_to_unfollow = User.query.filter_by(username=username).first()
    current_user.following.remove(user_to_unfollow)
    db.session.commit()
    return redirect(url_for('users.profile', username=user_to_unfollow.username))