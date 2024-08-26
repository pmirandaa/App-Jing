from rest_framework import status
from rest_framework.test import APITestCase

from Event.models import Event


class EventTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get Event instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_events_list(self):
        url = '/api/events/'
        expected = [
            {
                "id": 2,
                "name": "Jing 2021",
                "year": 2021,
                "logo": 'http://testserver/events/teddy-bear.png',
                'current': False
            }
            
            ,
            
            {
                "id": 1,
                "name": "Jing 2022",
                "year": 2022,
                "logo": 'http://testserver/events/teddy-bear.png',
                'current': False
            }
            
        ]
        response = self.client.get(url, format='json')
        print("Respuesta: ")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_event_instance(self):
        url = '/api/events/1/'
        expected = {
            "id": 1,
            "name": "Jing 2022",
            "year": 2022,
            "logo": "http://testserver/events/teddy-bear.png",
            'current': False
        }
        response = self.client.get(url, format='json')
        print("Respuesta: ")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update Event
    # ======================

    def test_create_event(self):
        url = '/api/events/'
        events_count = Event.objects.count()
        data = {
            "name": "Jing 2023",
            "year": 2023,
        }
        expected = {
            "id": events_count + 1,
            "name": "Jing 2023",
            "year": 2023,
            "logo": None,
            'current': False
        }
        response = self.client.post(url, data, format='json')
        print("Respuesta: ")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), events_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_event(self):
        url = '/api/events/1/'
        data = {
            "name": "Jing 2024",
            "year": 2024,
            # TODO: Update logo
        }
        expected = {
            "id": 1,
            "name": "Jing 2024",
            "year": 2024,
            "logo": "http://testserver/events/teddy-bear.png",
            'current': False
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)
