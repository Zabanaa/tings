from .test import BaseTestClass

wintermute = {"name": "my project"}
zabana     = {"name": "My Personal Site"}
incomplete = {"title": "my project"}

class TestProjectEndpoints(BaseTestClass):

    def test_get_all_projects(self):
        projects    = self.app.get('/api/projects')
        response    = self.decode_json(projects.data)
        assert projects.status_code == 200
        assert 'meta' in response
        assert 'count' in response['response']
        assert 'projects' in response['response']

    def test_get_projects_tasks(self):

        tasks       = self.app.get("/api/projects/1/tasks")
        response    = self.decode_json(tasks.data)

        assert tasks.status_code == 200
        assert 'count' in response['response']
        assert 'tasks' in response['response']
        assert isinstance(response['response']['tasks'], list)

    def test_get_projects_labels(self):

        labels       = self.app.get("/api/projects/1/labels")
        response     = self.decode_json(labels.data)

        assert labels.status_code == 200
        assert 'count' in response['response']
        assert 'labels' in response['response']
        assert isinstance(response['response']['labels'], list)

    def test_get_projects_done_tasks(self):

        tasks       = self.app.get("/api/projects/1/tasks/done")
        response    = self.decode_json(tasks.data)

        assert tasks.status_code == 200
        assert 'count' in response['response']
        assert 'tasks' in response['response']
        assert isinstance(response['response']['tasks'], list)

    def test_post_project(self):
        new_project = self.post('/api/projects', data=zabana)
        response    = self.decode_json(new_project.data)
        assert new_project.status_code == 201
        assert '/api/projects' in new_project.headers['location']
        assert 'meta' in response
        assert 'project' in response['response']

    def test_unique_name_violation(self):
        project_copy = self.post('/api/projects', data=wintermute)
        response     = self.decode_json(project_copy.data)
        expected_error_message = "(name) already exists"

        assert project_copy.status_code == 409
        assert response['meta']['type'] == 'error'
        assert response['response']['message'] == expected_error_message

    def test_post_with_missing_fields(self):
        new_project = self.post('/api/projects', data=incomplete)
        response    = self.decode_json(new_project.data)

        expected_error_message = 'Missing required fields.'
        assert new_project.status_code == 422
        assert response['meta']['type'] == 'error'
        assert response['response']['message'] == expected_error_message
        assert 'missing_fields' in response['response']

    def test_get_project_by_id(self):
        project           = self.app.get('/api/projects/1')
        response          = self.decode_json(project.data)
        tasks_dict_key    = response['response']['project']['tasks']


        assert project.status_code == 200
        assert response['meta']['type'] == 'success'

        project_data = response['response']['project']

        assert isinstance(project_data, dict)
        assert 'tasks' in response['response']['project']

        assert '/api/projects/1/tasks' in tasks_dict_key

    def test_get_non_existing_project(self):

        project  = self.app.get('/api/projects/3098713092183')
        response = self.decode_json(project.data)
        expected_error_msg = "Project not found"

        assert project.status_code == 404
        assert response['meta']['type'] == 'error'
        assert response['response']['message'] == expected_error_msg

    def test_update_project(self):
        data                 = {"name": "Wintermute v2"}
        updated_project      = self.put('/api/projects/1', data=data)
        response             = self.decode_json(updated_project.data)

        expected_response_message = "Update successful"

        assert updated_project.status_code == 200
        assert 'project' in response['response']
        assert response['response']['message'] == expected_response_message

    def test_update_project_wrong_id(self):
        data                    = {"name": "Wintermute v3"}
        updated_project         = self.put('/api/projects/883284', data=data)
        response                = self.decode_json(updated_project.data)

        expected_error_message = "Project not found"

        assert updated_project.status_code == 404
        assert response['meta']['type'] == 'error'
        assert response['response']['message'] == expected_error_message


    def test_update_project_unique_key_violation(self):
        new_project     = self.post('/api/projects', data=zabana)
        zabana_id       = self.decode_json(new_project.data)['response']['project']['id']

        updated_project  = self.put('/api/projects/2', data=wintermute)
        response         = self.decode_json(updated_project.data)

        expected_status_code    = 409
        expected_error_message  = "(name) already exists"

        assert updated_project.status_code        == expected_status_code
        assert response['response']['message']    == expected_error_message

    def test_delete_project(self):
        deleted_project          = self.app.delete('/api/projects/1')
        expected_status_code     = 204
        assert deleted_project.status_code == expected_status_code

        get_all_projects         = self.app.get('/api/projects')
        response                 = self.decode_json(get_all_projects.data)

        assert response['response']['count'] == 0

    def test_delete_non_existing_project(self):
        deleted_project          = self.app.delete('/api/projects/808')
        response                 = self.decode_json(deleted_project.data)

        expected_status_code        = 404
        expected_response_message   = "Project not found"

        assert deleted_project.status_code       == expected_status_code
        assert response['response']['message']   == expected_response_message
