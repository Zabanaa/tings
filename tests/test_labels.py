from .test import BaseTestClass

class TestLabelEndpoints(BaseTestClass):

    def test_get_all_labels(self):
        labels      = self.app.get('/api/labels')
        response    = self.decode_json(labels.data)

        expected_status_code = 200

        assert labels.status_code == expected_status_code
        assert 'count' in response['response']
        assert 'labels' in response['response']

    def test_get_label_by_id(self):
        label       = self.app.get('/api/labels/1')
        response    = self.decode_json(label.data)

        expected_status_code = 200

        assert label.status_code == expected_status_code
        assert 'label' in response['response']

    def test_get_label_wrong_id(self):
        label       = self.app.get('/api/labels/2')
        response    = self.decode_json(label.data)

        expected_status_code    = 404
        expected_error_message  = "Label not found"

        assert label.status_code == expected_status_code
        assert response['meta']['type'] == "error"
        assert response['response']['message'] == expected_error_message

    def test_post_label(self):
        data        = {"name": "my awesome label"}
        new_label   = self.post('/api/labels', data=data)
        response    = self.decode_json(new_label.data)

        expected_status_code            = 201
        expected_response_message       = "Label created"
        expected_location_header        = "/api/labels/2"

        response_message                = response['response']['message']
        response_location_header        = new_label.headers['location']

        assert new_label.status_code    == expected_status_code
        assert response_message         == expected_response_message
        assert expected_location_header in response_location_header
        assert 'label' in response['response']

    def test_post_label_missing_fields(self):
        data        = {}
        new_label   = self.post('/api/labels', data=data)
        response    = self.decode_json(new_label.data)

        expected_status_code        = 422
        expected_error_message      = "Missing required fields."
        expected_missing_fields     = ['color', 'name', 'project_id']

        response_message            = response['response']['message']
        response_missing_fields     = response['response']['missing_fields']

        assert new_label.status_code            == expected_status_code
        assert response_message                 == expected_error_message
        assert sorted(response_missing_fields)  == expected_missing_fields

        assert isinstance(response_missing_fields, list)

    def test_update_label(self):
        data            = {"name": "updated label"}
        updated_label   = self.put("/api/labels/1", data=data)
        response        = self.decode_json(updated_label.data)

        expected_label_name     = data['name']
        expected_status_code    = 200
        expected_response_message = "Update successful"

        response_message = response['response']['message']
        new_label_name   = response['response']['label']['name']

        assert updated_label.status_code == expected_status_code
        assert response_message          == expected_response_message
        assert new_label_name            == expected_label_name

    def test_update_label_wrong_id(self):
        data            = {"name": "updated label"}
        updated_label   = self.put("/api/labels/92832", data=data)
        response        = self.decode_json(updated_label.data)

        expected_status_code    = 404
        expected_error_message  = "Label not found"
        expected_response_type  = "error"

        response_message        = response['response']['message']
        response_type           = response['meta']['type']

        assert response_message          == expected_error_message
        assert response_type             == expected_response_type
        assert updated_label.status_code == expected_status_code

    def test_delete_label(self):

        deleted_label   = self.app.delete('/api/labels/1')

        expected_status_code    = 204
        assert deleted_label.status_code == expected_status_code

    def test_delete_label_wrong_id(self):
        deleted_label   = self.app.delete('/api/labels/09384038')
        response        = self.decode_json(deleted_label.data)

        expected_status_code    = 404
        expected_error_message  = "Label not found"
        expected_response_type  = "error"

        response_message        = response['response']['message']
        response_type           = response['meta']['type']

        assert response_message          == expected_error_message
        assert response_type             == expected_response_type
        assert deleted_label.status_code == expected_status_code

