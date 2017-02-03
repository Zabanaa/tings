from tings import app, db
from tings.api.models import Project, Task, Label
import json

class BaseTestClass(object):

    def setUp(self):
        app.config.from_object('tings.config.TestConfig')
        self.app = app.test_client()

        test_task    = Task({"name": "doing the tings"})
        test_project = Project({"name": "my project"})

        db.create_all()

        db.session.add(test_task)
        db.session.add(test_project)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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
