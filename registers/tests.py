from datetime import timedelta, datetime
from django.test import TestCase

from django.conf import settings
from django.urls import reverse
from rest_framework import status

from masters.models import Master
from registers.exceptions import NonWorkingTime, MasterIsBusy
from registers.models import Register
from registers.services import RegisterService
from tests.services import IsAuthClientTestCase, TestDataService
from rest_framework.test import APITestCase


REGISTER_CREATE_VIEW_NAME = 'registers:create'
REGISTER_RETRIEVE_VIEW_NAME = 'registers:retrieve_update_destroy'
REGISTER_LIST_VIEW_NAME = 'registers:list'


class RegisterServiceCheckIsWorkingTimeMethodTestCase(TestCase):
    test_data_service = TestDataService()

    def test_after_working_time(self):
        time = self.test_data_service.get_time_in_working_range().replace(hour=settings.WORKING_DAY_ENDS_AT_HOUR + 1)
        self.assertFalse(RegisterService.check_is_working_time(time))

    def test_before_working_time(self):
        time = self.test_data_service.get_time_in_working_range().replace(hour=settings.WORKING_DAY_STARTS_AT_HOUR - 1)
        self.assertFalse(RegisterService.check_is_working_time(time))

    def test_weekend_time(self):
        time = self.test_data_service.get_time_in_working_range()
        while time.weekday() not in settings.NON_WORKING_DAYS_OF_THE_WEEK:
            time += timedelta(days=1)
        self.assertFalse(RegisterService.check_is_working_time(time))

    def test_offset_before_working_time_end(self):
        time = self.test_data_service.get_time_in_working_range().replace(
            hour=settings.WORKING_DAY_ENDS_AT_HOUR - 1,
            minute=20
        )
        self.assertFalse(RegisterService.check_is_working_time(time))

    def test_before_now_time(self):
        time = datetime(2020, 1, 1, 12, 0, 0, 0)
        self.assertFalse(RegisterService.check_is_working_time(time))

    def test_working_time(self):
        time = self.test_data_service.get_time_in_working_range()
        self.assertTrue(RegisterService.check_is_working_time(time))


class RegisterCreateTestCase(IsAuthClientTestCase, APITestCase):
    test_data_service = TestDataService()
    master: Master

    def setUp(self):
        super().setUp()
        self.master = self.test_data_service.create_master()

    def test_create_register(self):
        data = {
            'start_at': self.test_data_service.get_time_in_working_range(),
        }
        response = self.client.post(reverse(REGISTER_CREATE_VIEW_NAME, args=(self.master.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        register = Register.objects.get(pk=response.data['pk'])
        self.assertEqual(register.master, self.master)
        self.assertEqual(register.user, self.user)
        self.assertEqual(register.start_at, data['start_at'])
        self.assertEqual(register.end_at, register.start_at + timedelta(hours=settings.REGISTER_LIFETIME))

    def test_fail_create_register_on_busy_time(self):
        start_at = self.test_data_service.get_time_in_working_range()
        self.test_data_service.create_register(self.user, self.master, start_at)
        data = {'start_at': start_at}

        response = self.client.post(reverse(REGISTER_CREATE_VIEW_NAME, args=(self.master.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), MasterIsBusy.default_detail)

    def test_fail_create_register_to_master_on_weekend(self):
        start_at = self.test_data_service.get_time_in_working_range()
        while start_at.weekday() not in settings.NON_WORKING_DAYS_OF_THE_WEEK:
            start_at += timedelta(days=1)

        data = {'start_at': start_at}

        response = self.client.post(reverse(REGISTER_CREATE_VIEW_NAME, args=(self.master.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), NonWorkingTime.default_detail)

    def test_fail_create_register_on_less_than_an_hour_before_busy_time(self):
        start_at = self.test_data_service.get_time_in_working_range(offset_after_in_hours=1)

        self.test_data_service.create_register(self.user, self.master,  start_at + timedelta(minutes=30))
        data = {'start_at': start_at}

        response = self.client.post(reverse(REGISTER_CREATE_VIEW_NAME, args=(self.master.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), MasterIsBusy.default_detail)

    def test_fail_create_register_on_less_than_an_hour_before_the_end_of_the_working_day(self):
        start_at = self.test_data_service.get_time_in_working_range()
        start_at = start_at.replace(hour=settings.WORKING_DAY_ENDS_AT_HOUR - 1, minute=30)
        print(start_at)

        data = {'start_at': start_at}

        response = self.client.post(reverse(REGISTER_CREATE_VIEW_NAME, args=(self.master.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), NonWorkingTime.default_detail)

    def test_fail_create_register_to_non_working_time(self):
        start_at = self.test_data_service.get_time_in_working_range()
        start_at = start_at.replace(hour=settings.WORKING_DAY_ENDS_AT_HOUR + 1)

        data = {'start_at': start_at}

        response = self.client.post(reverse(REGISTER_CREATE_VIEW_NAME, args=(self.master.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), NonWorkingTime.default_detail)


class RegisterDestroyTestCase(IsAuthClientTestCase, APITestCase):
    test_data_service = TestDataService()
    master: Master

    def setUp(self):
        self.master = self.test_data_service.create_master()

    def test_destroy_register(self):
        pass

    def test_fail_destroy_register_if_it_in_progress(self):
        pass

    def test_fail_destroy_register_if_it_already_ended(self):
        pass

class RegisterUpdateTestCase(IsAuthClientTestCase, APITestCase):
    test_data_service = TestDataService()
    master: Master

    def setUp(self):
        self.master = self.test_data_service.create_master()

    def test_update_register(self):
        pass

    def test_fail_update_register_if_it_in_progress(self):
        pass

    def test_fail_update_register_if_it_already_ended(self):
        pass

    def test_fail_update_register_time_to_busy_time(self):
        pass

    def test_fail_update_register_time_to_less_than_an_hour_before_busy_time(self):
        pass

    def test_fail_update_register_time_to_less_than_an_hour_before_the_end_of_the_working_day(self):
        pass

    def test_fail_update_register_time_to_after_working_time(self):
        pass


class RegisterTestCase(IsAuthClientTestCase, APITestCase):
    test_data_service = TestDataService()
    master: Master

    def setUp(self):
        self.master = self.test_data_service.create_master()

    def test_get_register_by_id(self):
        pass

    def test_get_request_user_registers_list(self):
        pass

    def test_get_master_registers_list(self):
        pass

    def test_get_dates_with_free_time(self):
        pass

    def test_dates_must_be_greater_than_now_when_get_dates_for_which_user_can_register(self):
        pass

    def test_get_specified_date_free_time(self):
        pass

    def test_time_must_be_greater_than_now_when_get_specified_date_free_time(self):
        pass
