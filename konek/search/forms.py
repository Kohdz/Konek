from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    text = StringField('Search',
                       validators=[InputRequired('Search query is Required')])
