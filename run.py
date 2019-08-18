from twitter_clone import app
from flask_migrate import Migrate, MigrateCommand
from twitter_clone import db
from flask_script import Manager


Migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# # 
if __name__ == "__main__":
    manager.run()
    # app.run(debug=True)