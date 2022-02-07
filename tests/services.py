import random
from abc import ABC
from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework.test import APIClient
from django.core.files import File
from django.conf import settings

import utils.random
from masters.models import Master
from registers.models import Register
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

    @staticmethod
    def create_register(user: User, master: Master, start_at: datetime = timezone.now()) -> Register:
        return Register.objects.create(user=user, master=master, start_at=start_at)

    @staticmethod
    def get_time_in_working_range(time: datetime = timezone.now() + timedelta(minutes=5),
                                  offset_before_in_hours: int = 0,
                                  offset_after_in_hours: int = 0, ) -> datetime:
        """
        Возвращает время, которое:
        - больше текущего
        - входит в рабочие дни
        - входит в рабочее время
        - оставляет запас на время процесса работы
        """

        now_time = timezone.now() + timedelta(minutes=5)

        if time < now_time:
            time = now_time

        working_day_starts_at_hour = settings.WORKING_DAY_STARTS_AT_HOUR + offset_before_in_hours
        working_day_ends_at_hour = \
            settings.WORKING_DAY_ENDS_AT_HOUR - settings.REGISTER_LIFETIME - offset_after_in_hours

        while not (working_day_starts_at_hour < time.hour <= working_day_ends_at_hour):
            time += timedelta(minutes=30)

        while time.weekday() in settings.NON_WORKING_DAYS_OF_THE_WEEK:
            time += timedelta(days=1)

        return time

    @staticmethod
    def get_tuesday() -> datetime:
        thu_date = timezone.now().replace(hour=settings.WORKING_DAY_STARTS_AT_HOUR, minute=0)
        # Ищем дату ближайшего вторника
        while thu_date.weekday() != 1:
            thu_date += timedelta(days=1)
        return thu_date

    def make_busy_day(self, user: User, master: Master, date: datetime) -> list[Register]:
        for hour in range(settings.WORKING_DAY_STARTS_AT_HOUR,
                          settings.WORKING_DAY_ENDS_AT_HOUR - settings.REGISTER_LIFETIME,
                          settings.REGISTER_LIFETIME):
            self.create_register(user, master, date.replace(hour=hour))


def get_test_jpg_picture() -> File:
    return get_file_rb(filename='test_picture.jpg', path=settings.TEST_FILES_ROOT)


def get_test_png_picture() -> File:
    return get_file_rb(filename='test_picture.png', path=settings.TEST_FILES_ROOT)
