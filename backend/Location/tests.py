from rest_framework import status
from rest_framework.test import APITestCase

from Location.models import Location


class LocationTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get Location instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_locations_list(self):
        url = '/api/locations/'
        expected = [
            {
                "id": 1,
                "name": "La Cancha",
                "address": "qwe 123",
                "university": 1
            },
            {
                "id": 2,
                "name": "Piscina",
                "address": "zxc 789",
                "university": 2
            },
        ]
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_location_instance(self):
        url = '/api/locations/1/'
        expected = {
            "id": 1,
            "name": "La Cancha",
            "address": "qwe 123",
            "university": 1
        }
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update Location
    # ======================

    def test_create_location(self):
        url = '/api/locations/'
        locations_count = Location.objects.count()
        data = {
            "name": "Gimnasio",
            "address": "Dirección 789",
            "university": 3
        }
        expected = {
            "id": locations_count + 1,
            "name": "Gimnasio",
            "address": "Dirección 789",
            "university": 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), locations_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_location(self):
        url = '/api/locations/1'
        data = {
            "name": "Dojo",
            "address": "Providencia 456",
            "university": 2
        }
        expected = {
            "id": 1,
            "name": "Dojo",
            "address": "Providencia 456",
            "university": 2
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)
