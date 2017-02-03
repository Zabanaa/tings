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
# @manager.option('-T', '--task-id')
# def create_task(name, project_id, task_id=None):
def create_task(name, project_id):
    t = Task({"name": name, "project_id": project_id})
    # t = Task({"name": name, "id": id, "task_id": task_id})
    db.session.add(t)
    db.session.commit()

@manager.option('-n', '--name')
@manager.option('-T', '--task-id')
def create_label(name, task_id):
    l = Label({"name": name, "task_id": task_id})
    db.session.add(l)
    db.session.commit()

if __name__ == "__main__":
    manager.run()
