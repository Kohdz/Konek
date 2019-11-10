from flask_login import LoginManager, UserMixin
from konek import db


followers = db.Table(
    'Followers', db.Column('follower_id', db.Integer,
                           db.ForeignKey('user.id')),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id')))

likes = db.Table('Likes',
    db.Column('user_id',  db.Integer, db.ForeignKey('user.id')),
    db.Column('tweet_id', db.Integer, db.ForeignKey('tweet.id'))
    )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(120), unique=True)
    image = db.Column(db.String(100), default='amon.png')
    password = db.Column(db.String(100))
    join_date = db.Column(db.DateTime)
    tweets = db.relationship('Tweet', backref='user', lazy='dynamic')

    following = db.relationship('User',
                                secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.following_id == id),
                                backref=db.backref('followed_by',
                                                   lazy='dynamic'),
                                lazy='dynamic')

    liked = db.relationship('Tweet', 
                            secondary=likes,
                            backref=db.backref('liked_by', lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        return f'username: {self.username} | name: {self.name} | email: {self.email}'


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(140))
    date_created = db.Column(db.DateTime)
    count = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f'tweet id: {self.id} | user id: {self.user_id} | tweet: {self.text}'


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))
    image = db.Column(db.String(100))
    name = db.Column(db.String(30))
    username = db.Column(db.String(30))
    text = db.Column(db.String(140))
    date_created = db.Column(db.DateTime)

    def __repr__(self):
        return f'reply id: {self.id} | reply text: {self.text} | user: {self.username} | tweet text: {self.tweet_id.text}'
