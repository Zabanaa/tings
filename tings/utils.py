from collections import namedtuple

Error       = namedtuple("Error", "status body headers")
Response    = namedtuple('Response', 'status body headers')

class Helpers(object):

    def get_all(cls):
        objects_name = "{}s".format(cls.__tablename__)
        objects      = [ obj.to_dict() for obj in cls.query.all() ]
        count        = len(objects)
        data         = {"count": count, objects_name: objects }

        return new_response(status_code=200, data=data)

    def get_one(cls, id):
        obj         = cls.query.get(id)
        obj_name    = cls.__tablename__

        if obj is None:
            message = "{} not found".format(obj_name.capitalize())
            return error_response(status_code=404, message=message)

        obj  = obj.to_dict()
        data = { obj_name: obj }
        return new_response(status_code=200, data=data)

    def create_new(cls, payload):

        obj_name = cls.__tablename__

        try:
            new_obj = cls(payload)
            new_project.save()
            json_project = new_project.to_dict()

            headers      = { "location": new_project.url }

            data         = {
                "project": json_project,
                "message": "Project successfully created."
            }

            return new_response(status_code=201, data=data, headers=headers)

        except Exception as e:
            cause_of_error = str(e.__dict__['orig'])
            if "violates unique constraint" in cause_of_error:
                message = "A project with that name already exists."
                return error_response(status_code=409, message=message)

            elif "not-null" in cause_of_error:
                missing_fields = get_missing_fields(e.__dict__['params'])
                return error_response(
                        status_code=422,
                        message="Missing required fields.",
                        missing_fields=missing_fields
                )
            else:
                message = "Something went wrong, please ask a developer for assistance"
                return error_response(status_code=500, message=message)

    def update(cls, payload):
        pass

    def delete(cls, id):
        obj         = cls.query.get(id)
        obj_name    = cls.__tablename__

        if obj is None:
            message = "{} not found".format(obj_name.capitalize())
            return error_response(status_code=404, message=message)

        obj.delete()
        return new_response(status_code=204)

def error_response(status_code=None, message=None, headers={}, missing_fields=None):
	response	= {}
	response['message'] = message

	if missing_fields:
		response['missing_fields'] = missing_fields

	meta        = { "type": "error", "status": status_code}
	body    	= { "meta": meta, "response": response }

	return Error(status=status_code, body=body, headers={})

def new_response(status_code=None, data={}, headers={}):
	meta         = { "type": "success", "status": status_code }
	body         = { "meta": meta, "response": data }
	headers      = headers
	return  Response(status=status_code, body=body, headers=headers)

def get_missing_fields(fields):

    missing_fields = []

    for key, value, in fields.items():
        if fields[key] == None:
            missing_fields.append(key)
    return missing_fields
