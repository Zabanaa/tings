from tings import db
from tings.database import Model
from flask import url_for

class Project(Model):

    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(50), unique=True, nullable=False)
    tasks    = db.relationship('Task', backref='project', lazy='dynamic')

    def __init__(self, payload):
        for key, value in payload.items():
            setattr(self, key, value)

    def to_dict(self):
        """
        Transforms the instance to a JSON formatted object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "tasks": "a link to the project's tasks",
            "href": self.url
        }

    @property
    def url(self):

        """
        Returns a full url to the instance's resource in the following form:
        https://tings.co/api/projects/<self.id>
        """
        return url_for('.get_project', project_id=self.id, _external=True)

    @property
    def tasks(self):

        """
            Returns a full url to GET all the tasks
            assigned to the current project
        """
        return url_for('.get_project_tasks', project_id=self.id, _external=True)

class Task(Model):

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    done        = db.Column(db.Boolean, default=False)
    project_id  = db.Column(db.Integer, db.ForeignKey('project.id'))
    label_id    = db.Column(db.Integer, db.ForeignKey('label.id'))

    def __init__(self, payload):
        for key, value in payload.items():
            setattr(self, key, value)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "done": self.done,
            "href": self.url,
            "project": self.parent_project,
            "label": "self.get_label()"
        }

    @property
    def url(self):
        """
        Returns a full url to the instance's resource in the following form:
        https://tings.co/api/tasks/<self.id>
        """
        return url_for('.get_task', task_id=self.id, _external=True)

    def get_label(self):
        return url_for('.get_label', label_id=self.label_id)

    @property
    def parent_project(self):
        if self.project_id is not None:
            return url_for('.get_project', project_id=self.project_id, _external=True)

        return "No project assigned"

class Label(Model):
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(40), unique=True)
    color   = db.Column(db.String(7))
    tasks   = db.relationship('Task', backref="label", lazy="dynamic")

    def __init__(self, payload):
        for key, value in payload.items():
            setattr(self, key, value)

    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "color": self.color,
    #         "href": self.get_url(),
    #         "tasks": self.get_takss()
    #     }

    # def get_url(self):
    #     return url_for('api.label', label_id=self.id)

    # def get_tasks(self):
    #     return url_for('api.task', label_id=self.id)
