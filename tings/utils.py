from collections import namedtuple

Error       = namedtuple("Error", "status_code body headers")
Response    = namedtuple('Response', 'status_code body headers')

def error_response(status_code=None, message=None, headers={}, missing_fields=None):
	response	= {}
	response['message'] = message

	if missing_fields:
		response['missing_fields'] = missing_fields

	meta        = { "type": "error", "status": status_code}
	body    	= { "meta": meta, "response": response }

	return Error(status_code=status_code, body=body, headers={})

def new_response(status_code=None, body={}, headers={}):
	meta        = { "type": "success", "status": status_code }
	res_body    = { "meta": meta, "response": body }
	headers     = headers
	return  Response(status_code=status_code, body=res_body, headers=headers)

def get_missing_fields(fields):

    missing_fields = []

    for key, value, in fields.items():
        if fields[key] == None:
            missing_fields.append(key)
    return missing_fields

def not_found_error(message):
    return error_response(status_code=404, message=message)

def missing_fields_error(fields):
    message = "Missing required fields."
    return  error_response(status_code=422, message=message, missing_fields=fields)

def unique_field_error():
    message = "Resource must be unique"
    return error_response(status_code=409, message=message)

def server_error():
    message = "Something bad happened"
    return error_response(status_code=500, message=message)

def forbidden_error():
    message = "You do not have permission to access this resource"
    return error_response(status_code=403, message=message)

def unauthorized_error():
    message = "You are not authorised to access this resource. Please sign up or login."
    return error_response(status_code=403, message=message)

def bad_request_error():
    message = "Bad request"
    return error_response(status_code=400, message=message)
