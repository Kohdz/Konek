import os


class Config:
    UPLOADED_PHOTOS_DEST = 'images'
    # joe's path to db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///twitterclone.db'
    SECRET_KEY = 'test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    #dir alternative to flask
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Vicktree/Desktop/twitter-clone2/konek/twitterclone.db'