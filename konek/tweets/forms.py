from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import InputRequired


class TweetForm(FlaskForm):
    text = TextAreaField('Message', validators=[InputRequired('Message is Required')])


class ReplyForm(FlaskForm):
    reply = TextAreaField('Enter your reply here', validators=[InputRequired('Comment is Required')])