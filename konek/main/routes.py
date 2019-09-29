from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash
from konek.search.forms import SearchForm
from konek import db, app, login_manager
from konek.models import User


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
    return render_template('index.html', title='Homepage')