from collections import namedtuple
from flask import jsonify
Response = namedtuple("Response", "status body headers")

def get_todos():
    response = Response(status=200, body="response body", headers=None)
    return response

def json(view_func):

    def inner(*args, **kwargs):

        """
        takes the returned response object from the view function
        and unpacks it into a JSON formatted object
        """

        # Unpack the tuple returned by the view function
        response = view_func(*args, **kwargs)
        status, body, headers = response

        # Create an empty object
        response_data           = {}
        response_data['status'] = status
        response_data['body']   = body

        # response = jsonify(response)

        # set response status code and headers
        # response.status_code = status

        # if headers is not None:
        #     response.headers.extend(headers)

        return response_data

    return inner

# print(get_todos())
get_todos = json(get_todos)
print(get_todos())
