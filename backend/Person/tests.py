import json
from pprint import pprint
from rest_framework import status
from rest_framework.test import APITestCase


class PersonTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get Placement instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_persons_list(self):
        url = '/api/persons/'
        expected = [
            {
                "id": 1,
                "place": 1,
                "participated": True,
                "sport": 1,
                "event": 1,
                "university": 1
            }
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_person_instance(self):
        url = '/api/persons/1/'
        expected = {
            "id": 1,
            "place": 1,
            "participated": True,
            "sport": 1,
            "event": 1,
            "university": 1
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_persons_filtered(self):
        url = '/api/persons/?event=1&last_name="Cisneros"&first_name="Sebastián"&university=1&sport=1&is_coord_sport=0&is_coord_uni=0'
        expected = [
            {
                "id": 1,
                "place": 1,
                "participated": True,
                "sport": 1,
                "event": 1,
                "university": 1
            }
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_person_filters(self):
        url = '/api/persons/filters/?event=1'
        expected = {
            'sport': [{'label': 'Fútbol', 'value': 1},
                      {'label': 'Básquetbol', 'value': 2}],
            'university': [{'label': 'UCH', 'value': 1},
                           {'label': 'PUC', 'value': 2},
                           {'label': 'UdeC', 'value': 3},
                           {'label': 'UdeC', 'value': 4}]
        }
        response = self.client.get(url, format='json')
        response_json = json.loads(response.content)
        pprint(response_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertJSONEqual(response.content, expected)

    # Create and update Placement
    # ======================

    def test_create_person(self):
        url = '/api/placements/'
        placements_count = Placement.objects.count()
        data = {
            "coordinator": 4,
            "university": 3,
            "sport": 2,
            "event": 2
        }
        expected = {
            "id": placements_count + 1,
            "coordinator": 4,
            "university": 3,
            "place": 0,
            "event_score": 0,
            "sport": 2,
            "event": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(response.content, expected)

    def test_update_person(self):
        url = '/api/placements/1/'
        data = {
            "coordinator": 4,
            "university": 3,
            "sport": 2,
            "event": 2
        }
        expected = {
            "id": 1,
            "coordinator": 4,
            "university": 3,
            "place": 1,
            "event_score": 2000,
            "sport": 2,
            "event": 2
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)
