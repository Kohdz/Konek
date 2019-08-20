from flask_login import LoginManager, UserMixin
# from twitter_clone import db
from . import db


# wont be acessing this class directly, no no class needed
# has relationship back to user
followers = db.Table('Followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'))
    )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30))
    email = db.Column(db.String(120))
    image = db.Column(db.String(100), default='amon.png')
    password = db.Column(db.String(50))
    join_date = db.Column(db.DateTime)
    tweets = db.relationship('Tweet', backref='user', lazy='dynamic')
    
    following = db.relationship('User', secondary=followers, 
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.following_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    followed_by = db.relationship('User', secondary=followers,
        primaryjoin=(followers.c.following_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        backref=db.backref('follower', lazy='dynamic'), lazy='dynamic')

    # format of return string of "User.query.__() terminal command"
    def __repr__(self):
        return f'username: {self.username} | name: {self.name} | email: {self.email}'


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(140))
    date_created = db.Column(db.DateTime)

    # format of return string of "Tweet.query.__() terminal command"
    def __repr__(self):
        return f'user id: {self.user_id} | tweet: {self.text}'
