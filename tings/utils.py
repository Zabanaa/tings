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


def not_found_error():
    # 404
    pass

def missing_fields_error():
    # 422
    pass

def unique_field_error():
    # 409
    pass

def server_error():
    # 500
    pass

def forbidden_error():
    # 401
    pass

def unauthorized_error():
    # 403
    pass

def bad_request_error():
    # 400
    pass

