from tings import app, db
from tings.decorators import jsonise
from tings.api.models import Project, Task, Label
import json

wintermute = {"name": "my project"}
zabana     = {"name": "My Personal Site"}

incomplete = {"title": "my project"}

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
        response    = self.decode_json(result.data)
        assert result.status_code == 200
        assert 'meta' in response
        assert 'count' in response['data']
        assert 'projects' in response['data']

    def test_post_project(self):

        result      = self.post('/api/projects', data=zabana)
        response    = self.decode_json(result.data)
        assert result.status_code == 201
        assert '/api/projects' in result.headers['location']
        assert 'meta' in response
        assert 'project' in response['data']

    def test_unique_name_violation(self):
        result      = self.post('/api/projects', data=wintermute)
        response    = self.decode_json(result.data)
        expected_error_message = 'A project with that name already exists.'

        assert result.status_code == 409
        assert response['meta']['type'] == 'error'
        assert response['response']['message'] == expected_error_message

    def test_post_with_missing_fields(self):
        result = self.post('/api/projects', data=incomplete)
        response = self.decode_json(result.data)

        expected_error_message = 'Missing required fields.'
        assert result.status_code == 422
        assert response['meta']['type'] == 'error'
        assert response['response']['message'] == expected_error_message
        assert 'missing_fields' in response['response']


