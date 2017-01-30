from tings import app, db
from tings.api.models import Project, Task, Label
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    from subprocess import call
    call('nosetests --nocapture', shell=True)

if __name__ == "__main__":
    manager.run()
