from twitter_clone import app
from flask_migrate import Migrate, MigrateCommand
from twitter_clone import db
from flask_script import Manager

MIGRATION_DIR = "./twitter_clone/migrations"
Migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# # 
if __name__ == "__main__":
    manager.run()
    # app.run(debug=True)