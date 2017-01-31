from collections import namedtuple

Error       = namedtuple("Error", "status body headers")
Response    = namedtuple('Response', 'status body headers')

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
	body         = { "meta": meta, "data": data }
	headers      = headers
	return  Response(status=status_code, body=body, headers=headers)

def get_missing_fields(fields):

	missing_fields = []
	for key, value, in fields.items():
		missing_fields.append(key)
	return missing_fields
