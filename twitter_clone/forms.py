from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
from wtforms import StringField, PasswordField, BooleanField
from flask_uploads import IMAGES
from twitter_clone.models import User


class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired('A full name is required.'),
         Length(max=100, message='Name Must Not Exceed 100 Charactors')])

    username = StringField('Username', validators=[InputRequired('Username is required'), 
        Length(max=30, message="Username Has Too Many Characters")])

    email = StringField('Email', validators=[InputRequired('Email is required'), Email()])

    password = PasswordField('Password', validators=[InputRequired('A password is required')])

    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

    image = FileField(validators=[FileAllowed(IMAGES, 'Only Images Are Accepted')])

    # method to check whether the user name is taken or not
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    remember = BooleanField('Remember me')