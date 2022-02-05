import random
from abc import ABC

from rest_framework.test import APIClient
from django.core.files import File
from django.conf import settings

import utils.random
from masters.models import Master
from utils.helper import get_file_rb
from users.models import User
from tokens.serializers import TokenObtainPairSerializer


class UserFactoryMixin:
    USER_PASSWORD = 'sdw332!4TdSD'
    CAR_MODEL = 'BMW'

    @staticmethod
    def __random_char(length=10, repeat=1):
        return ''.join(utils.random.random_simple_string(length) for _ in range(repeat))

    def create_user(self, email: str, first_name: str, second_name: str, **kwargs) -> 'User':
        if len(first_name) == 0:
            first_name = 'None'
        if len(second_name) == 0:
            second_name = 'None'
        user = User.objects.create_user(email=email, first_name=first_name, second_name=second_name,
                                        car_model=self.CAR_MODEL, password=self.USER_PASSWORD, **kwargs)
        user.save()
        return user

    def create_random_user(self, **kwargs) -> 'User':
        return self.create_user(email=self.__random_char() + "@gmail.com", first_name=self.__random_char(),
                                second_name=self.__random_char(), **kwargs)

    @staticmethod
    def create_client_with_auth(user: 'User') -> APIClient:
        token = TokenObtainPairSerializer.get_token(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer %s' % token.access_token)
        return client


class IsAuthClientTestCase(UserFactoryMixin, ABC):
    user: User
    client: APIClient

    staff_user: User
    staff_client: APIClient

    anonymous_client: APIClient

    def setUp(self):
        self.user = self.create_random_user()
        self.client = self.create_client_with_auth(self.user)

        self.staff_user = self.create_random_user(is_staff=True)
        self.staff_client = self.create_client_with_auth(user=self.staff_user)

        self.anonymous_client = self.client_class()


class TestDataService(UserFactoryMixin):
    @staticmethod
    def create_master(first_name: str = utils.random.random_simple_string(10),
                      second_name: str = utils.random.random_simple_string(10),
                      middle_name: str = utils.random.random_simple_string(10)) -> Master:
        return Master.objects.create(first_name=first_name, second_name=second_name, middle_name=middle_name)


def get_test_jpg_picture() -> File:
    return get_file_rb(filename='test_picture.jpg', path=settings.TEST_FILES_ROOT)


def get_test_png_picture() -> File:
    return get_file_rb(filename='test_picture.png', path=settings.TEST_FILES_ROOT)
