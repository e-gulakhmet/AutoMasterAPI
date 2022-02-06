from django.urls import reverse
from rest_framework import status

from tests.services import IsAuthClientTestCase, TestDataService
from rest_framework.test import APITestCase


REGISTER_CREATE_VIEW_NAME = 'registers:create'
REGISTER_RETRIEVE_VIEW_NAME = 'registers:retrieve_update_destroy'
REGISTER_LIST_VIEW_NAME = 'registers:list'


class MasterTestCase(IsAuthClientTestCase, APITestCase):
    test_data_service = TestDataService()

    def test_create_register(self):
        pass

    def test_fail_create_register_to_master_who_is_busy_on_specified_time(self):
        pass

    def test_fail_create_register_to_master_on_weekend(self):
        pass

    def test_fail_create_register_on_busy_time(self):
        pass

    def test_fail_create_register_on_less_than_an_hour_before_busy_time(self):
        pass

    def test_fail_create_register_on_less_than_an_hour_before_the_end_of_the_working_day(self):
        pass

    def test_fail_create_register_after_working_time(self):
        pass

    def test_destroy_register(self):
        pass

    def test_fail_destroy_register_if_it_in_progress(self):
        pass

    def test_fail_destroy_register_if_it_already_ended(self):
        pass

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

    # def test_retrieve_master_by_id(self):
    #     master = self.test_data_service.create_master()
    #     response = self.client.get(reverse(MASTER_RETRIEVE_VIEW_NAME, args=[master.pk]))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
    #     self.assertEqual(response.data['pk'], master.pk)
    #     self.assertEqual(response.data['first_name'], master.first_name)
    #     self.assertEqual(response.data['second_name'], master.second_name)
    #     self.assertEqual(response.data['middle_name'], master.middle_name)
