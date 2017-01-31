from tings import app
from tings.utils import new_response
from tings.decorators import jsonise
import json


def fake_view_func():
    return new_response(status_code=202, data={'id': 3}, headers={"someheader": "header"})

class TestDecorators(object):

    def setUp(self):
        app.config.from_object('tings.config.TestConfig')
        self.app = app.test_client()

    def tearDown(self):
        pass

    def decode_json(self, payload):
        return json.loads(payload.decode('utf-8'))

    def test_json(self):
        with app.test_request_context():

            status, body, headers   = fake_view_func()
            decorated_view          = jsonise(fake_view_func)

            response                = decorated_view()
            response_data           = self.decode_json(response.data)

            assert response.status_code == status
            assert response_data        == body
            for header in list(headers.keys()):
                assert header in response.headers
