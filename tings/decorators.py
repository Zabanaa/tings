from flask import jsonify

def jsonise(view_func):

    def wrapper(*args, **kwargs):

        """
        takes the returned response object from the view function
        and unpacks it into a JSON formatted object
        """

        # Unpack the tuple returned by the view function
        response = view_func(*args, **kwargs)
        status, body, headers = response

        # Create an empty object
        response_data           = body
        response = jsonify(response_data)

        # set response status code and headers
        response.status_code = status
        response.headers.extend(headers)

        return response

    return wrapper
