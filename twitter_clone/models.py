from flask_login import LoginManager, UserMixin
# from twitter_clone import db
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30))
    email = db.Column(db.String(120))
    image = db.Column(db.String(100))
    password = db.Column(db.String(50))
    join_date = db.Column(db.DateTime)




    # format of return string of "User.query.__() terminal command"
    def __repr__(self):
        return f'username: {self.username} | name: {self.name} | email: {self.email}'