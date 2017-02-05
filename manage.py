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

@manager.option('-n', '--name')
def create_project(name):
    p = Project({"name": name})
    db.session.add(p)
    db.session.commit()

@manager.option('-n', '--name', dest='name')
@manager.option('-P', '--project-id', dest='project_id')
@manager.option('-L', '--label-id')
def create_task(name, project_id, label_id=None):
    t = Task({"name": name, "project_id": project_id, "label_id": label_id})
    db.session.add(t)
    db.session.commit()

@manager.option('-n', '--name')
@manager.option('-P', '--project-id')
def create_label(name, project_id):
    l = Label({"name": name, "project_id": project_id})
    db.session.add(l)
    db.session.commit()

if __name__ == "__main__":
    manager.run()
