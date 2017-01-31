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

    def put(self, endpoint, data, content_type="application/json"):
        resp = self.app.put(
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
        assert 'count' in response['response']
        assert 'projects' in response['response']

    def test_post_project(self):

        result      = self.post('/api/projects', data=zabana)
        response    = self.decode_json(result.data)
        assert result.status_code == 201
        assert '/api/projects' in result.headers['location']
        assert 'meta' in response
        assert 'project' in response['response']

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

    def test_get_project_by_id(self):
        result   = self.app.get('/api/projects/1')
        response = self.decode_json(result.data)

        assert result.status_code == 200
        assert response['meta']['type'] == 'success'

        project = response['response']['project']

        assert isinstance(project, dict)
        assert 'tasks' in response['response']['project']

    def test_get_non_existing_project(self):

        result   = self.app.get('/api/projects/3098713092183')
        response = self.decode_json(result.data)
        expected_error_msg = "Project not found"

        assert result.status_code == 404
        assert response['meta']['type'] == 'error'
        assert response['response']['message'] == expected_error_msg

    def test_update_project(self):
        updated_project = {"name": "Wintermute v2"}
        result      = self.put('/api/projects/1', data=updated_project)
        response    = self.decode_json(result.data)

        expected_response_message = "Update successful"

        assert result.status_code == 200
        assert 'project' in response['response']
        assert response['response']['message'] == expected_response_message

    def test_update_project_wrong_id(self):

        updated_project = {"name": "Wintermute v3"}
        result      = self.put('/api/projects/883284', data=updated_project)
        response    = self.decode_json(result.data)

        expected_error_message = "Project not found"

        assert result.status_code == 404
        assert response['meta']['type'] == 'error'
        assert response['response']['message'] == expected_error_message


    def test_update_project_unique_key_violation(self):
        pass

    def test_delete_project(self):
        pass
