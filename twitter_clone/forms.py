from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
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
    
    # method to check whether the email is taken or not
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')


# update account settings form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    image = FileField(validators=[FileAllowed(IMAGES, 'Only Images Are Accepted')])
    email = StringField('Email', validators=[InputRequired('Email is required'), Email()])
    submit = SubmitField('Update')

    # method to check whether the user name is taken or not
    def validate_username(self, username):
       if username.data != current_user.username:
           user = User.query.filter_by(username=username.data).first()
           if user:
               raise ValidationError('That username is taken. Please choose a different one.')

    # method to check whether the user name is taken or not
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')


class TweetForm(FlaskForm):
    text = TextAreaField('Message', validators=[InputRequired('Message is Required')])


class ReplyForm(FlaskForm):
    reply = TextAreaField('Enter your reply here', validators=[InputRequired('Comment is Required')])


class SearchForm(FlaskForm):
    text = StringField('Search', validators=[InputRequired('Search query is Required')])