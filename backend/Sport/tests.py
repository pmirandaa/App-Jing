from rest_framework import status
from rest_framework.test import APITestCase

from Sport.models import Sport


class SportTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get Sport instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_sports_list(self):
        url = '/api/sports/'
        expected = [
            {
                "id": 1,
                "name": "Fútbol",
                "gender": "FEM",
                "sport_type": "A",
                "coordinator": 1,
                "closed": True
            },
            {
                "id": 2,
                "name": "Básquetbol",
                "gender": "MIX",
                "sport_type": "A",
                "coordinator": 2,
                "closed": False
            },
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_sport_instance(self):
        url = '/api/sports/1/'
        expected = {
            "id": 1,
            "name": "Fútbol",
            "gender": "FEM",
            "sport_type": "A",
            "coordinator": 2,
            "closed": True
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update Sport
    # ======================

    def test_create_sport(self):
        url = '/api/sports/'
        sports_count = Sport.objects.count()
        data = {
            "name": "Vóleibol",
            "gender": "MLE",
            "sport_type": "C",
            "coordinator": 3,
        }
        expected = {
            "id": sports_count + 1,
            "name": "Vóleibol",
            "gender": "MLE",
            "sport_type": "C",
            "coordinator": 3,
            "closed": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sport.objects.count(), sports_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_sport(self):
        url = '/api/sports/1/'
        data = {
            "name": "Tenis de mesa",
            "gender": "MIX",
            "sport_type": "B",
            "coordinator": 3
        }
        expected = {
            "id": 1,
            "name": "Tenis de mesa",
            "gender": "MIX",
            "sport_type": "B",
            "coordinator": 3,
            "closed": True
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)
