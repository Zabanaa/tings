from tings import app
from .test import BaseTestClass
from tings.utils import new_response
from tings.decorators import jsonise
import json

class TestDecorators(BaseTestClass):

    @jsonise
    def fake_view_func(self):
        data    = { "id": 3 }
        headers = { "someheader": "header" }
        return new_response(status_code=202, body=data, headers=headers)

    def test_jsonise_decorator(self):
        with app.test_request_context():

            response                = self.fake_view_func()
            response_data           = self.decode_json(response.data)

            expected_status_code    = 202
            expected_headers        = { "someheader": "header" }
            expected_data           = { "id": 3 }

            assert response.status_code             == expected_status_code
            assert response_data['response']        == expected_data

            for expected_header in list(expected_headers.keys()):
                assert expected_header in response.headers
