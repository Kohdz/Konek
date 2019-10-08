import os


class Config:
    UPLOADED_PHOTOS_DEST = 'images'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///konek.db'
    SECRET_KEY = 'test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')