from tings import app
from collections import namedtuple
from tings.decorators import jsonise
import json

Response = namedtuple("APIResp", "status body headers")

def fake_view_func():
    response = Response(status=202, body={'id': 3}, headers={"someheader": "header"})
    return response


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

            fake_view_response = fake_view_func()
            decorated_view = jsonise(fake_view_func)
            response = decorated_view()
            data = self.decode_json(response.data)

            assert data['status']       == fake_view_response[0]
            assert data['body']         == fake_view_response[1]
            assert response.status_code == fake_view_response[0]
            for header in list(fake_view_response[2].keys()):
                assert header in response.headers
