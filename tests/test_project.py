from tings import app, db
from tings.decorators import jsonise
from tings.api.models import Project, Task, Label
import json

wintermute = {"name": "my project"}
zabana     = {"name": "My Personal Site"}

class TestProjectEndpoints(object):

    def setUp(self):
        app.config.from_object('tings.config.TestConfig')
        self.app = app.test_client()
        db.create_all()
        project = Project(wintermute)
        db.session.add(project)
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

    def test_get_all_projects(self):
        result      = self.app.get('/api/projects')
        response    = self.decode_json(result.data)['data']
        assert result.status_code == 200
        assert 'meta' in response
        assert 'count' in response['data']
        assert 'projects' in response['data']

    def test_post_project(self):
        result      = self.post('/api/projects', data=zabana)
        response    = self.decode_json(result.data)['data']
        assert result.status_code == 201
        assert 'meta' in response
        assert 'project' in response['data']
        assert 'href' in response['data']['project']
        assert '/api/projects' in result.headers['location']
