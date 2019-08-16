from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField
from wtforms.validators import InputRequired, Length 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Vicktree/Desktop/twitter-clone/twitterclone.db'
app.config['SECRET_KEY'] = 'test'


db = SQLAlchemy(app)
Migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30))
    image = db.Column(db.String(100))
    password = db.Column(db.String(50))

class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired('A full name is required.'), Length(max=100, message='Name Must Not Exceed 100 Charactors')])
    username = StringField('Username', validators=[InputRequired('Username is required'), Length(max=30, message="Username Has Too Many Characters")])
    password = PasswordField('Password', validators=[InputRequired('A password is required')])
    image = FileField()


@app.route('/')
def index():
    return render_template('index.html')

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
        return '<h1>Name: {}, Username: {}, Password: {}</h1>'.format(form.name.data, form.username.data, form.password.data)
    return render_template('register.html', form=form)


if __name__ == '__main__':
    manager.run()