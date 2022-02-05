from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.exceptions import InvalidToken

from tests.services import IsAuthClientTestCase


TOKEN_VERIFY_VIEW_NAME = 'tokens:verify'
TOKEN_OBTAIN_PAIR_VIEW_NAME = 'tokens:obtain_pair'
TOKEN_CHECK_AUTH_VIEW_NAME = 'tokens:check_auth'


class TokenTestCase(IsAuthClientTestCase, APITestCase):
    credentials: dict

    def setUp(self) -> None:
        super().setUp()
        self.credentials = {
            'email': self.user.email,
            'password': self.USER_PASSWORD,
        }

    def test_get_token(self):
        response = self.client.post(reverse(TOKEN_OBTAIN_PAIR_VIEW_NAME), self.credentials)
        tokens = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertTrue(tokens['access'])
        self.assertTrue(tokens['refresh'])

        response = self.client.post(reverse(TOKEN_VERIFY_VIEW_NAME), {'token': tokens['access']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % tokens['access'])
        auth_client = self.client_class()
        auth_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % tokens['access'])

        response = auth_client.post(reverse(TOKEN_CHECK_AUTH_VIEW_NAME))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_token_verify(self):
        access = 'eyJ0eXAiOiJKV1p2LCJhbGciOiJIUzI1NiJ9.' \
                 'eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwI' \
                 'joxNTg0Nzg1NDkxLCJqdGkiOiI3NDkyNzdlOG' \
                 'E0MzU0NDk5OTY2ZjFjZWI2ZDhlNGRmNSIsInV' \
                 'zZXJfaWQiOjV9.EDuzYiPjtyn9WrMcrueZC9IV0BTmWciq9U2TBFMIpw0'

        response = self.client.post(reverse(TOKEN_VERIFY_VIEW_NAME), {'token': access})
        self.assertEqual(response.status_code, InvalidToken.status_code, response.data)
        self.assertEqual(response.data['detail'], InvalidToken.default_detail)
        self.assertEqual(response.data['code'], InvalidToken.default_code)

    def test_fail_email_get_token(self):
        data = self.credentials
        data['email'] = 'te3st23@exam22ple.ru'

        response = self.client.post(reverse(TOKEN_OBTAIN_PAIR_VIEW_NAME), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_password_get_token(self):
        data = self.credentials
        data['password'] = 'te3stasdasd'

        response = self.client.post(reverse(TOKEN_OBTAIN_PAIR_VIEW_NAME), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_password_and_email_get_token(self):
        data = self.credentials
        data['email'] = 'te3s45t23@exam2d2ple.ru'
        data['password'] = 'te3stas4332dasd'

        response = self.client.post(reverse(TOKEN_OBTAIN_PAIR_VIEW_NAME), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_token_for_admin_access_user(self):
        anonymous_client = self.client_class()
        credentials = {
            'email': self.staff_user.email,
            'password': self.USER_PASSWORD,
        }

        response = anonymous_client.post(reverse(TOKEN_OBTAIN_PAIR_VIEW_NAME), credentials)
        tokens = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertTrue(tokens['access'])
        self.assertTrue(tokens['refresh'])

        response = anonymous_client.post(reverse(TOKEN_VERIFY_VIEW_NAME), {'token': tokens['access']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        anonymous_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % tokens['access'])

        response = anonymous_client.post(reverse(TOKEN_CHECK_AUTH_VIEW_NAME))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
