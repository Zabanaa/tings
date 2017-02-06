from tings import db
from tings.database import Model
from tings.utils import new_response
from flask import url_for

class Project(Model):

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), unique=True, nullable=False)
    tasks       = db.relationship('Task', backref='project', lazy='dynamic')
    labels      = db.relationship('Label', backref='project', lazy='dynamic')

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
            "tasks": self.tasks,
            "labels": self.labels,
            "href": self.url
        }

    @property
    def tasks(self):

        """
            Returns a full url to GET all the tasks
            assigned to the current project
        """
        return url_for('.get_project_tasks', id=self.id, _external=True)

    @property
    def labels(self):
        """
            Returns a full url to GET all the labels
            created in a project.
        """
        return url_for('.get_project_labels', id=self.id, _external=True)

    @classmethod
    def get_labels(cls, project_id):

        _labels = Label.query.filter_by(project_id=project_id).all()

        labels  = [l.to_dict() for l in _labels]
        count   = len(labels)
        data    = { "count": count, "labels": labels }
        return new_response(status_code=200, body=data)

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
            "label": self.label
        }

    @property
    def label(self):
        if self.label_id:
            return url_for(".get_label", id=self.label_id, _external=True)
        else:
            return "No label assigned"

class Label(Model):
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(40), nullable=False)
    color           = db.Column(db.String(7))
    project_id      = db.Column(db.Integer, db.ForeignKey('project.id'))
    tasks           = db.relationship('Task', backref="label", lazy="dynamic")

    def __init__(self, payload):
        for key, value in payload.items():
            setattr(self, key, value)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "href": self.url,
            "project": self.parent_project,
            "tasks": self.tasks
        }

    @property
    def tasks(self):
        return url_for(".get_label_tasks", id=self.id, _external=True)

