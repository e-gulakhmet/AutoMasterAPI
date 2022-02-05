from django.urls import reverse
from rest_framework import status

from tests.services import IsAuthClientTestCase, TestDataService
from rest_framework.test import APITestCase

from users.models import User


USER_REGISTER_VIEW_NAME = 'users:register'


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
            'car_model': self.CAR_MODEL
        }

    def test_registration(self):
        response = self.client.post(reverse(USER_REGISTER_VIEW_NAME), data=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.credentials['email'])
        self.assertEqual(user.is_active, True)

    def test_fail_register_already_registered_email(self):
        self.test_data_service.create_user(self.credentials['email'],
                                           self.credentials['first_name'],
                                           self.credentials['second_name'])

        response = self.client.post(reverse(USER_REGISTER_VIEW_NAME), data=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        user = User.objects.get(email=self.credentials['email'])
        self.assertEqual(user.is_active, True)
