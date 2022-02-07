from django.urls import reverse
from rest_framework import status

from tests.services import IsAuthClientTestCase, TestDataService
from rest_framework.test import APITestCase

from users.models import User


USER_REGISTER_VIEW_NAME = 'users:register'
USER_ME_VIEW_NAME = 'users:me'
USER_CHANGE_PASSWORD_VIEW_NAME = 'users:change_password'


class UserRegistrationTestCase(IsAuthClientTestCase, APITestCase):
    test_data_service = TestDataService()

    credentials: dict

    def setUp(self):
        super().setUp()
        self.credentials = {
            'first_name': 'Foo',
            'second_name': 'Bar',
            'email': 'test@test.ru',
            'password': self.USER_PASSWORD,
            'car_model': self.CAR_MODEL,
            'middle_name': 'Down'
        }

    def test_registration(self):
        response = self.client.post(reverse(USER_REGISTER_VIEW_NAME), data=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.credentials['email'])
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.first_name, self.credentials['first_name'])
        self.assertEqual(user.second_name, self.credentials['second_name'])
        self.assertEqual(user.middle_name, self.credentials['middle_name'])
        self.assertEqual(user.car_model, self.credentials['car_model'])

    def test_fail_register_already_registered_email(self):
        self.test_data_service.create_user(self.credentials['email'],
                                           self.credentials['first_name'],
                                           self.credentials['second_name'])

        response = self.client.post(reverse(USER_REGISTER_VIEW_NAME), data=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_fail_register_with_wrong_email_format(self):
        pass


class UserPasswordTestCase(IsAuthClientTestCase, APITestCase):
    def test_change_password(self):
        data = {
            'password': self.USER_PASSWORD,
            'new_password': 'New_password123',
        }

        response = self.client.post(reverse(USER_CHANGE_PASSWORD_VIEW_NAME), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(data['new_password']))

    def test_fail_change_password_with_wrong_old_password(self):
        data = {
            'password': 'Wrong_password',
            'new_password': 'New_password123',
        }

        response = self.client.post(reverse(USER_CHANGE_PASSWORD_VIEW_NAME), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(data['new_password']))


class UserTestCase(IsAuthClientTestCase, APITestCase):
    test_data_service = TestDataService()

    def test_get_user_me(self):
        response = self.client.get(reverse(USER_ME_VIEW_NAME))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['pk'], self.user.pk)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['second_name'], self.user.second_name)
        self.assertEqual(response.data['car_model'], self.user.car_model)

    def test_update_user_first_name(self):
        data = {
            'first_name': 'Newfirstname',
        }

        response = self.client.patch(reverse(USER_ME_VIEW_NAME), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['pk'], self.user.pk)
        self.assertEqual(response.data['first_name'], data['first_name'])

    def test_update_user_second_name(self):
        data = {
            'second_name': 'Newsecondname',
        }
        response = self.client.patch(reverse(USER_ME_VIEW_NAME), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['pk'], self.user.pk)
        self.assertEqual(response.data['second_name'], data['second_name'])

    def test_update_user_middle_name(self):
        data = {
            'middle_name': 'Newmiddlename',
        }
        response = self.client.patch(reverse(USER_ME_VIEW_NAME), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['pk'], self.user.pk)
        self.assertEqual(response.data['middle_name'], data['middle_name'])

    def test_update_user_car_model(self):
        data = {
            'car_model': 'New Car Model',
        }
        response = self.client.patch(reverse(USER_ME_VIEW_NAME), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['pk'], self.user.pk)
        self.assertEqual(response.data['car_model'], data['car_model'])
