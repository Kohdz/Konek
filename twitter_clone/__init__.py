from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads
from flask_login import LoginManager
from flask_uploads import IMAGES


app = Flask(__name__)

# manually traverse folder or import as global alies
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
#dir alternative to flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Vicktree/Desktop/twitter-clone2/twitter_clone/twitterclone.db'
                                                
# joe's path to db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitterclone.db'

app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

login_manager = LoginManager(app)
login_manager.login_view = 'login'

configure_uploads(app, photos)

db = SQLAlchemy(app)
Migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from twitter_clone import routes