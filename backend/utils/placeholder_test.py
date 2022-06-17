from rest_framework import status
from rest_framework.test import APITestCase

from Placeholder.models import Placeholder


class PlaceholderTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get Placeholder instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_placeholders_list(self):
        url = '/api/placeholders/'
        expected = [
            {
                "id": 1,
            },
            {
                "id": 2,
            },
            {
                "id": 3,
            }
        ]
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_placeholder_instance(self):
        url = '/api/placeholders/1/'
        expected = {
            "id": 1,
        }
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update Placeholder
    # ======================

    def test_create_placeholder(self):
        url = '/api/placeholders/'
        placeholders_count = Placeholder.objects.count()
        data = {
        }
        expected = {
            "id": placeholders_count + 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Placeholder.objects.count(), placeholders_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_placeholder(self):
        url = '/api/placeholders/1'
        data = {
        }
        expected = {
            "id": 1,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)
