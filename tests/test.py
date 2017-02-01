from tings import app, db
from tings.api.models import Task
import json

class BaseTestClass(object):

    def decode_json(self, payload):
        return json.loads(payload.decode('utf-8'))

    def post(self, endpoint, data, content_type="application/json"):
        resp = self.app.post(
        endpoint,
        data=json.dumps(data),
        content_type=content_type,
        follow_redirects=True
        )
        return resp

    def put(self, endpoint, data, content_type="application/json"):
        resp = self.app.put(
        endpoint,
        data=json.dumps(data),
        content_type=content_type,
        follow_redirects=True
        )
        return resp
