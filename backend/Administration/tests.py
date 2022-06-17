from rest_framework import status
from rest_framework.test import APITestCase

from Administration.models import Log


class LogTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get Log instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_logs_list(self):
        # TODO define fixture and test, these values are just placeholders
        url = '/api/logs/'
        expected = [
            {
                "id": 1,
                "task": "create_person",
                "value_before": "-",
                "value_after": "Yop Yop",
                "person": "Sebastián Cisneros",
                "date": "2021-10-06T11:49:02.402000-03:00"
            },
            {
                "id": 2,
                "task": "create_sport",
                "value_before": "None",
                "value_after": "Fútbol Femenino",
                "person": "Sebastián Cisneros",
                "date": "2021-10-06T11:49:25.098000-03:00"
            },
        ]
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_log_instance(self):
        # TODO define fixture and test, these values are just placeholders
        url = '/api/logs/1/'
        expected = {
            "id": 1,
            "task": "create_person",
            "value_before": "-",
            "value_after": "Yop Yop",
            "person": "Sebastián Cisneros",
            "date": "2021-10-06T11:49:02.402000-03:00"
        }
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update Log
    # ======================

    def test_create_log(self):
        # TODO define fixture and test, these values are just placeholders
        url = '/api/logs/'
        logs_count = Log.objects.count()
        data = {
            "task": "create_person",
            "value_before": "111 111",
            "value_after": "Yop Yop",
            "person": "Sebastián Cisneros",
            "date": "2022-06-03T12:00:00.000000-03:00"
        }
        expected = {
            "id": logs_count + 1,
            "task": "create_person",
            "value_before": "-",
            "value_after": "Yop Yop",
            "person": "Sebastián Cisneros",
            "date": "2022-06-03T12:00:00.000000-03:00"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Log.objects.count(), logs_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_log(self):
        url = '/api/logs/1'
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
