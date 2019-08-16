from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length
from wtforms import StringField, PasswordField, BooleanField
from flask_uploads import IMAGES


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