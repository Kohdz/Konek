from konek import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

MIGRATION_DIR = "./konek/migrations"
Migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
    # app.run(debug=True)
