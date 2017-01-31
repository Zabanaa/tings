from tings.utils import error_response, new_response, get_missing_fields

missing_fields_payload = { "name": None, "age": 22, "location": None }

class TestUtils(object):

    def setUp(self):
        self.missing_fields = get_missing_fields(missing_fields_payload)

    def test_error_response(self):

        expected_code = 409
        expected_msg = "Conflict. Shit Happened"

        err = error_response(status_code=expected_code, message=expected_msg)
        status_code, body, headers = err

        assert status_code == expected_code
        assert body['response']['message'] == expected_msg
        assert headers == {}

    def test_error_response_missing_fields(self):

        expected_code = 422
        expected_msg  = "Missing required fields"
        err = error_response(
                status_code=expected_code,
                message=expected_msg,
                missing_fields=self.missing_fields
        )
        status_code, body, headers = err

        assert body['response']['message'] == expected_msg
        assert status_code == expected_code
        assert headers     == {}
        assert 'missing_fields' in body['response']

    def test_new_response(self):
        expected_code    = 200
        expected_message = "Succcess"
        expected_body    = {"projects": [1, 2, 3]}
        expected_headers = {"X-Custom-Header": "Some value"}
        response = new_response(
                    status_code=200,
                    data=expected_body,
                    headers=expected_headers
        )

        status_code, body, headers = response

        assert status_code == expected_code
        assert body['response'] == expected_body
        assert headers == expected_headers

    def test_get_missing_fields(self):

        fields = self.missing_fields
        assert isinstance(fields, list)
        assert len(fields) == 2
