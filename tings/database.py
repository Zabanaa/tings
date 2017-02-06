from tings import db
from tings.utils import *
from flask import url_for
from sqlalchemy.exc import IntegrityError

class ModelMixin(object):

    @classmethod
    def create(cls, payload):
        """ Instantiates a new object
            and inserts it into the db
        """
        return cls(payload).save()

    def save(self):
        """saves the instance to the database"""
        try:
            db.session.add(self)
            db.session.commit()

        except IntegrityError as e:
            return self.handle_exception(e)

        else:
            message      = "{} created".format(self.obj_name).capitalize()
            headers      = { "location": self.url }
            data         = {
                self.obj_name: self.to_dict(),
                "message": message
            }
            return new_response(status_code=201, body=data, headers=headers)

    @classmethod
    def update(cls, payload, id):
        """Accepts a payload in the form of a dict
           Loops through it and updates the instance
           with the new values.
        """
        obj = cls.query.get(id)
        obj_name = cls.__tablename__

        if obj is None:
            message = "{} not found".format(obj_name.capitalize())
            return not_found_error(message)

        try:
            for key, value in payload.items():
                setattr(obj, key, value)
            db.session.commit()

        except IntegrityError as e:
            return cls.handle_exception(e)

        else:
            json_obj    = obj.to_dict()
            data        = {
                "message": "Update successful",
                obj_name: json_obj
            }
            return new_response(status_code=200, body=data)

    @classmethod
    def delete(cls, id):
        """ Accepts an <int> id.
            finds the corresponding resource
            and removes if from the db
        """
        obj = cls.query.get(id)
        obj_name = cls.__tablename__

        if obj is None:

            message = "{} not found".format(obj_name.capitalize())
            return not_found_error(message)

        db.session.delete(obj)
        db.session.commit()
        return new_response(status_code=204)

    @classmethod
    def get_all(cls):

        """
            When called, it will query the database
            and fetch the objects
            It will then proceed to serialise each object
            and return them in a list
        """

        objects_name = "{}s".format(cls.__tablename__)
        objects = [o.to_dict() for o in cls.query.all()]

        count        = len(objects)
        data         = {"count": count, objects_name: objects }

        return new_response(status_code=200, body=data)

    @classmethod
    def get_one(cls, id):
        """
            Accepts an <int> it.
            Fetches and returns the corresponding resource
            in dict format.
        """
        obj         = cls.query.get(id)
        obj_name    = cls.__tablename__

        if obj is None:
            message = "{} not found".format(obj_name.capitalize())
            return not_found_error(message)

        obj  = obj.to_dict()
        data = { obj_name: obj }
        return new_response(status_code=200, body=data)

    @classmethod
    def handle_exception(cls, exc):
        """ Accepts an exception
            returns the correct response depending
            on the cause of the error
        """
        cause_of_error = str(exc.__dict__['orig'])
        if "unique" in cause_of_error:
            key = cause_of_error.split("DETAIL: ")[1].split("=")[0].split(" ")[2]
            return unique_field_error(key)
        elif "not-null" in cause_of_error:
            missing_fields = get_missing_fields(exc.__dict__['params'])
            return missing_fields_error(missing_fields)
        else:
            return server_error()

    @classmethod
    def get_tasks(cls, **kwargs):

        from tings.api.models import Task

        _tasks = Task.query.filter_by(**kwargs).all()

        tasks  = [t.to_dict() for t in _tasks]
        count  = len(tasks)
        data   = { "count": count, "tasks": tasks }
        return new_response(status_code=200, body=data)

    @property
    def parent_project(self):
        if self.project_id is not None:
            return url_for('.get_project', id=self.project_id, _external=True)

        return "No project assigned"

    @property
    def as_dict(self):
        """creates a dict out of the instance's keys"""
        pass

    @property
    def obj_name(self):
        """ Returns the name of the class calling the method in lowercase"""
        return self.__tablename__

    @property
    def url(self):
        url_to_call = "tings_api.get_{}".format(self.obj_name)
        return url_for(url_to_call, id=self.id, _external=True)

    def __repr__(self):
        """ changes how the object is displayed in the shell"""
        obj_name = self.obj_name.capitalize()
        return "{} #{} - {}".format(obj_name, self.id, self.name)

class Model(ModelMixin, db.Model):
    __abstract__ = True
