from rest_framework import status
from rest_framework.test import APITestCase


class SportPlacementTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get Placement instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_sport_placements_list(self):
        url = '/api/placements/sport/'
        expected = [
            {
                "id": 1,
                "place": 1,
                "participated": True,
                "sport": 1,
                "event": 1,
                "university": 1
            },
            {
                "id": 2,
                "place": 2,
                "participated": True,
                "sport": 1,
                "event": 1,
                "university": 2
            },
            {
                "id": 3,
                "place": 2,
                "participated": True,
                "sport": 1,
                "event": 1,
                "university": 3
            },
            {
                "id": 4,
                "place": 4,
                "participated": False,
                "sport": 1,
                "event": 1,
                "university": 4
            }
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_sport_placement_instance(self):
        url = '/api/placements/sport/1/'
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

    def test_get_sport_placement_calculate(self):
        url = '/api/placements/sport/calculate/1/?event=1'
        expected = {
            "open_matches": 3,
            "results": [
                {
                    "university": 2,
                    "matches": 4,
                    "wins": 0,
                    "score": 21,
                    "attended": 0,
                    "participated": False,
                    "place": 1,
                    "points": 0
                },
                {
                    "university": 1,
                    "matches": 4,
                    "wins": 0,
                    "score": 16,
                    "attended": 0,
                    "participated": False,
                    "place": 2,
                    "points": 0
                },
                {
                    "university": 3,
                    "matches": 0,
                    "wins": 0,
                    "score": 0,
                    "attended": 0,
                    "participated": False,
                    "place": 3,
                    "points": 0
                },
                {
                    "university": 4,
                    "matches": 0,
                    "wins": 0,
                    "score": 0,
                    "attended": 0,
                    "participated": False,
                    "place": 3,
                    "points": 0
                }
            ]
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update Placement
    # ======================

    def test_create_sport_placement(self):
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
        self.assertEqual(Placement.objects.count(), placements_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_sport_placement(self):
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


class EventPlacementTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get Placement instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_event_placements_list(self):
        url = '/api/placements/event/'
        expected = [
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_event_placement_instance(self):
        url = '/api/placements/event/1/'
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

    def test_get_event_placement_calculate(self):
        self.maxDiff = None
        url = '/api/placements/event/calculate/1/'
        expected = {
            'event_placements': [
                {'event': 1, 'place': 1, 'points': 4000, 'university': 1},
                {'event': 1, 'place': 2, 'points': 3200, 'university': 2},
                {'event': 1, 'place': 3, 'points': 1920, 'university': 3},
                {'event': 1, 'place': 4, 'points': 0, 'university': 4}
            ],
            'sport_placements': {
                '1': [{'event': 1,
                       'participated': True,
                       'place': 1,
                       'points': 2000,
                       'sport': 1,
                       'university': 1},
                      {'event': 1,
                       'participated': True,
                       'place': 2,
                       'points': 1200,
                       'sport': 1,
                       'university': 2},
                      {'event': 1,
                       'participated': True,
                       'place': 2,
                       'points': 1200,
                       'sport': 1,
                       'university': 3},
                      {'event': 1,
                       'participated': False,
                       'place': 4,
                       'points': 0,
                       'sport': 1,
                       'university': 4}],
                '2': [{'attended': 1,
                       'matches': 3,
                       'participated': True,
                       'place': 1,
                       'points': 2000,
                       'score': 10,
                       'university': 1,
                       'wins': 0},
                      {'attended': 3,
                       'matches': 3,
                       'participated': True,
                       'place': 1,
                       'points': 2000,
                       'score': 10,
                       'university': 2,
                       'wins': 0},
                      {'attended': 2,
                       'matches': 2,
                       'participated': True,
                       'place': 3,
                       'points': 720,
                       'score': 8,
                       'university': 3,
                       'wins': 0},
                      {'attended': 0,
                       'matches': 0,
                       'participated': False,
                       'place': 4,
                       'points': 0,
                       'score': 0,
                       'university': 4,
                       'wins': 0}]
            }
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update Placement
    # ======================

    def test_create_event_placement(self):
        url = '/api/placements/event'
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
        self.assertEqual(Placement.objects.count(), placements_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_event_placement(self):
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
