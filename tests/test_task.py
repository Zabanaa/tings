from .test import BaseTestClass

test_task = {"name": "doing the tings"}
my_task   = {"name": "tings to do blud"}

class TestTaskEndpoints(BaseTestClass):

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
        task            = self.app.get('/api/tasks/1')
        response        = self.decode_json(task.data)
        task_project    = response['response']['task']['project']

        expected_status_code = 200
        assert task.status_code == expected_status_code
        assert 'meta' in response
        assert 'task' in response['response']
        assert task_project == "No project assigned" or "/api/projects/" in task__project

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

    def test_delete_task(self):
        deleted_task = self.app.delete('/api/tasks/1')
        expected_status_code = 204

        assert deleted_task.status_code == expected_status_code

    def test_delete_task_wrong_id(self):
        deleted_task = self.app.delete('/api/tasks/03802932')
        response     = self.decode_json(deleted_task.data)
        expected_status_code = 404
        expected_error_message = "Task not found"

        assert deleted_task.status_code == expected_status_code
        assert response['response']['message'] == expected_error_message
