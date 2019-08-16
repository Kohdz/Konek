from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Vicktree/Desktop/twitter-clone/twitterclone.db'
app.config['SECRET_KEY'] = 'test'

login_manager = LoginManager(app)



configure_uploads(app, photos)

db = SQLAlchemy(app)
Migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30))
    image = db.Column(db.String(100))
    password = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired('A full name is required.'),
         Length(max=100, message='Name Must Not Exceed 100 Charactors')])
    
    username = StringField('Username', validators=[InputRequired('Username is required'), 
        Length(max=30, message="Username Has Too Many Characters")])
    
    password = PasswordField('Password', validators=[InputRequired('A password is required')])
    image = FileField(validators=[FileAllowed(IMAGES, 'Only Images Are Accepted')])

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    remember = BooleanField('Remember me')


@app.route('/')
def index():

    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>Username: {}, Password: {}, Remember: {}</h1>'.format(form.username.data, form.password.data, form.remember.data)

    return render_template('index.html', form=form)

@app.route('/login', methods=['POST'])
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

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

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
    
    return render_template('register.html', form=form)


if __name__ == '__main__':
    manager.run()