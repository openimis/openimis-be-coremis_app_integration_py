import base64

from rest_framework import status
from rest_framework.test import APITestCase

from coremis_app_integration.tests.login_mixin import LogInMixin


TEST_LOGIN = {
  "username": "TestUserTest2",
  "password": "TestPasswordTest2%"
}

TEST_LOGIN_BAD_CREDENTIALS = {
  "username": "TestUserxxxxxxTest2",
  "password": "TestPassxxxxxxwordTest2%"
}


TEST_LOGIN_BAD_PAYLOAD = {
  "username2": "TestUserTest2",
  "password": "TestPasswordTest2%"
}


class LoginTests(APITestCase, LogInMixin):
    base_url = '/api/coremis_app_integration/api/mobile/v1/user/login'
    _test_request_data = None
    _test_request_data_wrong_credentials = None
    _test_request_data_bad_payload = None
    _headers = None

    def setUp(self):
        super(LoginTests, self).setUp()
        self._test_request_data = TEST_LOGIN
        self._test_request_data_wrong_credentials = TEST_LOGIN_BAD_CREDENTIALS
        self._test_request_data_bad_payload = TEST_LOGIN_BAD_PAYLOAD
        credentials = f"{TEST_LOGIN['username']}:{TEST_LOGIN['password']}"
        token = base64.b64encode(credentials.encode()).decode()
        basic_auth_token = f"Basic {token}"
        self._headers = {
            'HTTP_AUTHORIZATION': f'{basic_auth_token}',
        }

    def get_bundle_from_json_response(self, response):
        pass

    def test_post_should_create_correctly(self):
        self.get_or_create_user_api()
        response = self.client.post(
            self.base_url, data=self._test_request_data, format='json', **self._headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_should_give_unathorized(self):
        response = self.client.post(
            self.base_url, data=self._test_request_data_wrong_credentials, format='json', **self._headers
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_should_give_bad_payload(self):
        response = self.client.post(
            self.base_url, data=self._test_request_data_bad_payload, format='json', **self._headers
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_should_required_login(self):
        pass
