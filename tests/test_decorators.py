from tings import app
from .test import BaseTestClass
from tings.utils import new_response
from tings.decorators import jsonise
import json

class TestDecorators(BaseTestClass):

    def fake_view_func(self):
        data = { "id": 3 }
        headers={ "someheader": "header" }
        return new_response( status_code=202, data=data, headers = headers)

    def test_jsonise_decorator(self):
        with app.test_request_context():

            status, body, headers   = fake_view_func()
            decorated_view          = jsonise(fake_view_func)

            response                = decorated_view()
            response_data           = self.decode_json(response.data)

            assert response.status_code == status
            assert response_data        == body

            for header in list(headers.keys()):
                assert header in response.headers
