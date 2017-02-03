from tings import db
from sqlalchemy.exc import IntegrityError
from tings.utils import error_response, new_response, get_missing_fields

class ModelMixin(object):

    @classmethod
    def get_all(cls):
        objects_name = "{}s".format(cls.__tablename__)
        objects = [o.to_dict() for o in cls.query.all()]

        count        = len(objects)
        data         = {"count": count, objects_name: objects }

        return new_response(status_code=200, data=data)

    @classmethod
    def get_one(cls, id):
        obj         = cls.query.get(id)
        obj_name    = cls.__tablename__

        if obj is None:
            message = "{} not found".format(obj_name.capitalize())
            return error_response(status_code=404, message=message)

        obj  = obj.to_dict()
        data = { obj_name: obj }
        return new_response(status_code=200, data=data)

    @classmethod
    def create(cls, payload):
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
            return new_response(status_code=201, data=data, headers=headers)

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
            return error_response(status_code=404, message=message)

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
            return new_response(status_code=200, data=data)

    @classmethod
    def delete(cls, id):
        """deletes the instance from the database"""
        obj = cls.query.get(id)
        obj_name = cls.__tablename__

        if obj is None:

            message = "{} not found".format(obj_name.capitalize())
            return error_response(status_code=404, message=message)

        db.session.delete(obj)
        db.session.commit()
        return new_response(status_code=204, data={})

    @property
    def as_dict(self):
        """creates a dict out of the instance's keys"""
        pass

    @property
    def obj_name(self):
        return self.__tablename__

    @classmethod
    def handle_exception(cls, exc):
        cause_of_error = str(exc.__dict__['orig'])
        if "unique" in cause_of_error:
            message = "Resource must be unique"
            return error_response(status_code=409, message=message)

        elif "not-null" in cause_of_error:
            missing_fields = get_missing_fields(exc.__dict__['params'])
            return error_response(
                    status_code=422,
                    message="Missing required fields.",
                    missing_fields=missing_fields
                )
        else:
            message = "Something went wrong, please ask a developer for assistance"
            return error_response(status_code=500, message=message)

class Model(ModelMixin, db.Model):
    __abstract__ = True

