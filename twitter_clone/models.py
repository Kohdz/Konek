from flask_login import UserMixin
from twitter_clone import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30))
    image = db.Column(db.String(100))
    password = db.Column(db.String(50))
