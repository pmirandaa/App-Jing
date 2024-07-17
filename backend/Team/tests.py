from rest_framework import status
from rest_framework.test import APITestCase

from Team.models import Team
from Team.serializers import TeamSerializer, TeamTestSerializer
from django.http import JsonResponse, HttpResponse
import json


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
               'id': 1,
               'sport': {'id': 1, 'name': 'Fútbol', 'gender': 'FEM', 'sport_type': 'A'},
               "university":  {'id': 1, 'name': 'Universidad de Chile', 'city': 'Santiago', 'logo': None, 'map': None, 'short_name': 'UCH'}, 
               "coordinator": {'id': 3, 'user': None, 'name': '111', 'last_name': '111', 'email': 'asdf@asdf.asdf', 'university': 1, 'rut': '2-7', 'phone_number': '321654987', 'emergency_phone_number': '1', 'pending_messages': 0},
                'sport_name': 'Fútbol',
                "place": 0,      
                "event": 1,
            },
            {
                'id': 2,
                'sport': {'id': 1, 'name': 'Fútbol', 'gender': 'FEM', 'sport_type': 'A'}, 
                'university': {'id': 2, 'name': 'Universidad Católica', 'city': 'Santiago', 'logo': None, 'map': None, 'short_name': 'PUC'}, 
                'sport_name': 'Fútbol',
                'coordinator': {'id': 4, 'user': None, 'name': 'Juana', 'last_name': 'Perez', 'email': 'zxc@zxc.com', 'university': 2, 'rut': '3-5', 'phone_number': '123', 'emergency_phone_number': None, 'pending_messages': 0},
                'place': 0,
                'event': 1
             },
            {
                "id": 3,
                "sport": {'id': 2, 'name': 'Básquetbol', 'gender': 'MIX', 'sport_type': 'A'},
                "university": {'id': 3, 'name': 'Universidad de Concepción', 'city': 'Concepción', 'logo': None, 'map': None, 'short_name': 'UdeC'},
                "coordinator": {'id': 2, 'user': None, 'name': 'Yop', 'last_name': 'Yop', 'email': 'zxc@zxc.zxc', 'university': 3, 'rut': '1-9', 'phone_number': '12345678', 'emergency_phone_number': None, 'pending_messages': 0},
                'sport_name': 'Básquetbol',
                "place": 0,
                "event": 1,
            }
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        team1=Team.objects.get(pk=1)
        ser1=TeamSerializer(team1)
        team2=Team.objects.get(pk=2)
        ser2=TeamSerializer(team2)
        team3=Team.objects.get(pk=3)
        ser3=TeamSerializer(team3)
        # array=[ser1.data,ser2.data,ser3.data]
        string=json.loads(response.content)["results"]
        print("String\n")
        print(string)
        # #crear nuevo serialzador
        # print(string[0])
        # print(string)
        array=[]
        for elemento in string:
            array.append(elemento)
        print("Array\n")
        print(array)
        serie=TeamSerializer(array, many=True)
        print("Serie\n")
        print(serie)
        # print(serie.data)
        response=JsonResponse([string[0],string[1],string[2]], safe=False)
        # print(serie)
        # print(serie.data)
        self.assertJSONEqual(response.content, expected)

    def test_get_team_instance(self):
        url = '/api/teams/1/'
        expected = {
            "id": 1,
            "coordinator": 3,
            "university": 1,
            "place": 1,
            "sport": 1,
            "event": 1
        }
        response = self.client.get(url, format='json')
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

    def test_get_team_filters(self):
        url = '/api/teams/filters/?event=1'
        expected = {'gender': [{'label': 'Masculino', 'value': 'MLE'},
                               {'label': 'Femenino', 'value': 'FEM'},
                               {'label': 'Mixto', 'value': 'MIX'}],
                    'sport': [{'label': 'Fútbol', 'value': 1},
                              {'label': 'Básquetbol', 'value': 2}],
                    'sport_type': [{'label': 'Tipo A', 'value': 'A'},
                                   {'label': 'Tipo B', 'value': 'B'},
                                   {'label': 'Tipo C', 'value': 'C'}],
                    'universities': [{'label': 'UCH', 'value': 1},
                                     {'label': 'PUC', 'value': 2},
                                     {'label': 'UdeC', 'value': 3},
                                     {'label': 'UV', 'value': 4}]}
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
            "sport": 2,
            "event": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), teams_count + 1)
        team=Team.objects.get(pk=teams_count + 1)
        ser=TeamSerializer(team)
        self.assertJSONEqual(response.content, expected)

    def test_update_team(self):
        url = '/api/teams/1/'
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
            "sport": 2,
            "event": 2
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        team=Team.objects.get(pk=1)
        ser=TeamSerializer(team)
        
        self.assertJSONEqual(response.content, ser.data)
