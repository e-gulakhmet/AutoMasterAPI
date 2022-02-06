from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from tests.services import IsAuthClientTestCase, TestDataService
from rest_framework.test import APITestCase


MASTER_RETRIEVE_VIEW_NAME = 'masters:retrieve'
MASTER_LIST_VIEW_NAME = 'masters:list'


class MasterTestCase(IsAuthClientTestCase, APITestCase):
    test_data_service = TestDataService()

    def test_retrieve_master_by_id(self):
        master = self.test_data_service.create_master()
        response = self.client.get(reverse(MASTER_RETRIEVE_VIEW_NAME, args=[master.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['pk'], master.pk)
        self.assertEqual(response.data['first_name'], master.first_name)
        self.assertEqual(response.data['second_name'], master.second_name)
        self.assertEqual(response.data['middle_name'], master.middle_name)

    def test_get_masters_list(self):
        masters = [self.test_data_service.create_master() for _ in range(10)]

        response = self.client.get(reverse(MASTER_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['count'], len(masters))
        self.assertTrue(
            {result['pk'] for result in response.data['results']}
            &
            {master.pk for master in masters}
        )

    def test_get_master_free_time(self):
        pass

    def test_time_must_be_greater_than_now_when_get_master_free_time(self):
        pass

    # def test_get_masters_filtered_by_free_on_specified_date(self):
    #     busy_master = self.test_data_service.create_master(first_name='Busy')
    #     free_master = self.test_data_service.create_master(first_name='Free')
    #
    #     free_at = timezone.now() + timedelta(days=2)
    #     # Добавить запись для busy master на указанное время free_at
    #
    #     response = self.client.get(reverse(MASTER_LIST_VIEW_NAME), {'free_at': free_at})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
    #     self.assertEqual(response.data['count'], 1)
    #     self.assertEqual(response.data['results'][0]['pk'], free_master.pk)