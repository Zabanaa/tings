from flask import jsonify

def jsonise(view_func):

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

        response = jsonify(response_data)

        # set response status code and headers
        response.status_code = status

        if headers is not None:
            response.headers.extend(headers)

        return response

    return inner

