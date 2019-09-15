from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads
from flask_login import LoginManager
from flask_uploads import IMAGES
from konek.config import Config

app = Flask(__name__)
app.config.from_object(Config)
photos = UploadSet('photos', IMAGES)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

configure_uploads(app, photos)

db = SQLAlchemy(app)
Migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from konek.main.routes import main
from konek.users.routes import users
from konek.search.routes import search
from konek.tweets.routes import tweets

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(search)
app.register_blueprint(tweets)
