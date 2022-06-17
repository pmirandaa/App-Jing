from rest_framework import status
from rest_framework.test import APITestCase

from Team.models import Team


class TeamTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get Team instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_teams_list(self):
        url = '/api/teams/'
        expected = [
            {
                "id": 1,
                "coordinator": 3,
                "university": 1,
                "place": 1,
                "event_score": 2000,
                "sport": 1,
                "event": 1,
            },
            {
                "id": 2,
                "coordinator": 4,
                "university": 2,
                "place": 2,
                "event_score": 1200,
                "sport": 1,
                "event": 1,
            },
            {
                "id": 3,
                "coordinator": 2,
                "university": 3,
                "place": 0,
                "event_score": 0,
                "sport": 1,
                "event": 1,
            }
        ]
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_team_instance(self):
        url = '/api/teams/1/'
        expected = {
            "id": 1,
            "coordinator": 3,
            "university": 1,
            "place": 1,
            "event_score": 2000,
            "sport": 1,
            "event": 1
        }
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_team_players(self):
        url = '/api/teams/1/players'
        expected = [
            {
                "player_id": 4,
                "name": "Juana",
                "last_name": "Perez",
            },
            {
                "player_id": 5,
                "name": "Gabriel",
                "last_name": "Boric",
            }
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update Team
    # ======================

    def test_create_team(self):
        url = '/api/teams/'
        teams_count = Team.objects.count()
        data = {
            "coordinator": 4,
            "university": 3,
            "sport": 2,
            "event": 2
        }
        expected = {
            "id": teams_count + 1,
            "coordinator": 4,
            "university": 3,
            "place": 0,
            "event_score": 0,
            "sport": 2,
            "event": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), teams_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_team(self):
        url = '/api/teams/1'
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
