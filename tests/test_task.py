from .test import BaseTestClass
from tings import app, db
from tings.api.models import Task
import json

test_task = {"name": "doing the tings"}
my_task   = {"name": "tings to do blud"}

class TestProjectEndpoints(BaseTestClass):

    def setUp(self):
        app.config.from_object('tings.config.TestConfig')
        self.app = app.test_client()
        db.create_all()
        task = Task(test_task)
        db.session.add(task)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_tasks(self):
        tasks     = self.app.get('/api/tasks')
        response  = self.decode_json(tasks.data)

        expected_status_code = 200
        assert tasks.status_code == expected_status_code
        assert 'meta' in response
        assert 'count' in response['response']
        assert 'tasks' in response['response']

    def test_post_new_task(self):

        new_task = self.post('/api/tasks', data=my_task)
        response = self.decode_json(new_task.data)

        expected_status_code = 201

        assert new_task.status_code == expected_status_code
        assert '/api/tasks' in new_task.headers['location']
        assert 'meta' in response
        assert 'task' in response['response']

    def test_post_missing_fields(self):

        new_task = self.post('/api/tasks', data={})
        response = self.decode_json(new_task.data)

        expected_status_code    = 422
        expected_error_message = "Missing required fields."

        assert new_task.status_code             == expected_status_code
        assert response['response']['message']  == expected_error_message

    def test_get_task_by_id(self):
        task        = self.app.get('/api/tasks/1')
        response    = self.decode_json(task.data)

        expected_status_code = 200
        assert task.status_code == expected_status_code
        assert 'meta' in response
        assert 'task' in response['response']

    def test_get_task_wrong_id(self):

        task        = self.app.get('/api/tasks/37232')
        response    = self.decode_json(task.data)

        expected_status_code    = 404
        expected_error_message  = "Task not found"

        assert task.status_code                 == expected_status_code
        assert response['response']['message']  == expected_error_message

    def test_update_task(self):
        task_data   = {"name": "updated task"}
        task        = self.put('/api/tasks/1', data=task_data)
        response    = self.decode_json(task.data)

        expected_status_code    = 200

        assert task.status_code == expected_status_code
        assert response['response']['task']['name'] == task_data['name']
