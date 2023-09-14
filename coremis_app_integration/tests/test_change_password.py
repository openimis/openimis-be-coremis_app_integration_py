import base64

from rest_framework import status
from rest_framework.test import APITestCase

from coremis_app_integration.tests.login_mixin import LogInMixin


TEST_LOGIN = {
  "username": "TestUserTest2",
  "password": "TestPasswordTest2%"
}


TEST_CHANGE_PASSWORD = {
  "oldpassword": "TestPasswordTest2%",
  "newpassword": "TestPasswordTest23%",
  "confirmpassword": "TestPasswordTest23%"
}


TEST_CHANGE_PASSWORD_BAD_OLD_PASSWORD = {
  "oldpassword": "TestPasswordTest2dsds",
  "newpassword": "TestPasswordTest23",
  "confirmpassword": "TestPasswordTest23"
}


TEST_CHANGE_PASSWORD_BAD_CONFIRM_PASSWORD = {
  "oldpassword": "TestPasswordTest2",
  "newpassword": "TestPasswordTest23",
  "confirmpassword": "TestPasswordTest234"
}


class ChangePasswordTests(APITestCase, LogInMixin):
    base_url = '/api/coremis_app_integration/api/mobile/v1/user/password/change'
    _test_request_data = None
    _test_request_data_bad_old_password = None
    _test_request_data_bad_confirm_password = None
    _headers = None

    def setUp(self):
        super(ChangePasswordTests, self).setUp()
        self._test_request_data = TEST_CHANGE_PASSWORD
        self._test_request_data_bad_old_password = TEST_CHANGE_PASSWORD_BAD_OLD_PASSWORD
        self._test_request_data_bad_confirm_password = TEST_CHANGE_PASSWORD_BAD_CONFIRM_PASSWORD
        credentials = f"{TEST_LOGIN['username']}:{TEST_LOGIN['password']}"
        token = base64.b64encode(credentials.encode()).decode()
        basic_auth_token = f"Basic {token}"
        self._headers = {
            'HTTP_AUTHORIZATION': f'{basic_auth_token}',
        }

    def test_post_should_create_correctly(self):
        self.get_or_create_user_api()
        response = self.client.post(
            self.base_url, data=self._test_request_data, format='json', **self._headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_should_give_unathorized(self):
        self.get_or_create_user_api()
        response = self.client.post(
            self.base_url, data=self._test_request_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_should_give_bad_old_password(self):
        self.get_or_create_user_api()
        response = self.client.post(
            self.base_url, data=self._test_request_data_bad_old_password, format='json', **self._headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_should_give_bad_confirm_password(self):
        self.get_or_create_user_api()
        response = self.client.post(
            self.base_url, data=self._test_request_data_bad_confirm_password, format='json', **self._headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
