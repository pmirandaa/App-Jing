import json
from re import match
from unittest import skip
from rest_framework import status
from rest_framework.test import APITestCase

from Match.models import Match, MatchTeam


class MatchTest(APITestCase):
    fixtures = ['fixture.json']

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    # Create and update Match
    # =======================

    def test_create_match(self):
        self.maxDiff = None
        url = '/api/matches/'
        matches_count = Match.objects.count()
        match_teams_count = MatchTeam.objects.count()
        data = {
            "location": 1,
            "event": 1,
            "date": "2022-05-21T03:40",
            "teams": [{"team_id": 1}, {"team_id": 2}],
            "sport": 1,
            # This below shouldn't do anything
            "state": "MIF",
            "closed": True,
            "time_closed": "2021-12-21T04:09:50.726000-03:00",
            "winner": 1,
        }
        expected = {
            "id": matches_count + 1,
            "location": 2,
            "event": 1,
            "length": 0,
            "date": "2022-05-21T03:40:00-04:00",
            "sport": 1,
            "teams": [
                {
                    "match_team_id": match_teams_count + 1,
                    "team_id": 1,
                    "score": 0,
                    "comment": ""
                },
                {
                    "match_team_id": match_teams_count + 2,
                    "team_id": 2,
                    "score": 0,
                    "comment": ""
                }
            ],
            "state": "MTB",
            "closed": False,
            "time_closed": None,
            "winner": None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), matches_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_match_info(self):
        self.maxDiff = None
        url = '/api/matches/1/'
        data = {
            "location": 2,
            "event": 2,
            "length": 60,
            "date": "2022-05-22T03:40",
            "sport": 2,
            # This below shouldn't do anything
            "state": "MTB",
            "closed": False,
            "time_closed": "2022-01-01T06:00:00.000Z",
            "winner": 2
        }
        expected = {
            "id": 1,
            "location": 2,
            "event": 2,
            "length": 60,
            "date": "2022-05-22T03:40:00-04:00",
            "sport": 2,
            "teams": [
                {
                    "match_team_id": 1,
                    "team_id": 1,
                    "score": 1,
                    "comment": ""
                },
                {
                    "match_team_id": 2,
                    "team_id": 2,
                    "score": 2,
                    "comment": ""
                }
            ],
            "state": "MIF",
            "closed": True,
            "time_closed": "2021-12-21T04:09:50.726000-03:00",
            "winner": 1
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_update_match_teams(self):
        self.maxDiff = None
        url = '/api/matches/1/'
        data = {
            "teams": [{"match_team_id": 1, "team_id": 3, "score": 3},
                      {"team_id": 2, "score": 4}]
        }
        expected_teams = [
            {
                "match_team_id": 1,
                "team_id": 3,
                "score": 3,
                "comment": ""
            },
            {
                "match_team_id": 2,
                "team_id": 2,
                "score": 4,
                "comment": ""
            }
        ]
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = json.loads(response.content)
        self.assertIn('teams', response_json)
        self.assertEqual(response_json['teams'], expected_teams)

    # Start Match
    # ===========

    @skip
    def test_start_match(self):
        url = '/api/matches/2/start'
        expected = {
            "id": 2,
            "state": "MIC",
        }
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)
        match = Match.objects.get(id=2)
        self.assertFalse(match.closed)
        self.assertIsNone(match.time_closed)

    @skip
    def test_start_match_already_started(self):
        url = '/api/matches/3/start'
        expected = {
            "id": 3,
            "state": "MIC",
        }
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertJSONEqual(response.content, expected)
        match = Match.objects.get(id=3)
        self.assertFalse(match.closed)
        self.assertIsNone(match.time_closed)

    @skip
    def test_start_match_already_finished(self):
        url = '/api/matches/1/start'
        expected = {
            "id": 1,
            "state": "MIF",
            "closed": True,
            "time_closed": "2021-12-21T07:09:50.726Z",
        }
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertJSONEqual(response.content, expected)

    # Finish Match
    # ============

    @skip
    def test_finish_match(self):
        url = '/api/matches/3/finish'
        data = {
            "teams": [{"team_id": 1, "score": 7, "comment": "team 1 comment"},
                      {"team_id": 2, "score": 8, "comment": "team 2 comment"}],
            "winner": 2,
        }
        expected = {
            "id": 3,
            "teams": [
                {
                    "match_team_id": 5,
                    "team_id": 1,
                    "match": 3,
                    "score": 7,
                    "comment": "team 1 comment"
                },
                {
                    "match_team_id": 6,
                    "team_id": 2,
                    "match": 3,
                    "score": 8,
                    "comment": "team 2 comment"
                }
            ],
            "state": "MIF",
            "closed": True,
            "winner": 2,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = json.loads(response.content)
        self.assertIn('time_closed', response_json)
        self.assertIsNotNone(response_json.pop('time_closed'))
        self.assertEqual(response_json, expected)

    @skip
    def test_finish_match_already_finished(self):
        url = '/api/matches/1/finish'
        data = {
            "teams": [{"team_id": 1, "score": 7, "comment": "team 1 comment"},
                      {"team_id": 2, "score": 8, "comment": "team 2 comment"}],
            "winner": 2,
        }
        expected = {
            "id": 1,
            "state": "MIF",
            "closed": True,
            "time_closed": "2021-12-21T07:09:50.726Z",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertJSONEqual(response.content, expected)
        # Scores and winner should not have changed
        match = Match.objects.get(id=1)
        self.assertEqual(match.match_teams[0].score, 1)
        self.assertEqual(match.match_teams[1].score, 2)
        self.assertEqual(match.winner, 1)

    # Close Match
    # ===========

    @skip
    def test_close_match(self):
        url = '/api/matches/4/close'
        data = {
            "teams": [{"team_id": 1, "score": 7, "comment": "team 1 comment"},
                      {"team_id": 2, "score": 8, "comment": "team 2 comment"}],
            "winner": 2,
        }
        expected = {
            "id": 4,
            "teams": [
                {
                    "match_team_id": 5,
                    "team_id": 1,
                    "match": 4,
                    "score": 7,
                    "comment": "team 1 comment"
                },
                {
                    "match_team_id": 6,
                    "team_id": 2,
                    "match": 4,
                    "score": 8,
                    "comment": "team 2 comment"
                }
            ],
            "state": "MIF",
            "closed": True,
            "winner": 2,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = json.loads(response.content)
        self.assertIn('time_closed', response_json)
        self.assertIsNotNone(response_json.pop('time_closed'))
        self.assertEqual(response_json, expected)

    @skip
    def test_close_match_already_closed(self):
        url = '/api/matches/1/close'
        data = {
            "teams": [{"team_id": 1, "score": 7, "comment": "team 1 comment"},
                      {"team_id": 2, "score": 8, "comment": "team 2 comment"}],
            "winner": 2,
        }
        expected = {
            "id": 1,
            "state": "MIF",
            "closed": True,
            "time_closed": "2021-12-21T07:09:50.726Z",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertJSONEqual(response.content, expected)
        # Scores and winner should not have changed
        match = Match.objects.get(id=1)
        self.assertEqual(match.match_teams[0].score, 1)
        self.assertEqual(match.match_teams[1].score, 2)
        self.assertEqual(match.winner, 1)
