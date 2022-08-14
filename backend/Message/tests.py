import json
from rest_framework import status
from rest_framework.test import APITestCase

from Message.models import Message


class MessageTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get Message instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_messages_list(self):
        url = '/api/messages/'
        expected = [
            {
                "id": 1,
                "sender": 2,
                "reciever": 1,
                "event": 1,
                "subject": "Asd",
                "body": "Zxc",
                "is_read": True,
                "date": "2022-05-04T12:01:16.446Z",
                "deleted": False
            }
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_message_instance(self):
        url = '/api/messages/1/'
        expected = {
            "id": 1,
            "sender": 2,
            "reciever": 1,
            "event": 1,
            "subject": "Asd",
            "body": "Zxc",
            "is_read": True,
            "date": "2022-05-04T12:01:16.446Z",
            "deleted": False
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update Message
    # ======================

    def test_create_message(self):
        url = '/api/messages/'
        messages_count = Message.objects.count()
        data = {
            "sender": 1,
            "reciever": 2,
            "event": 1,
            "subject": "Mensaje de prueba",
            "body": "Hola! Este es un mensaje de prueba.",
        }
        expected = {
            "id": messages_count + 1,
            "sender": 1,
            "reciever": 2,
            "event": 1,
            "subject": "Mensaje de prueba",
            "body": "Hola! Este es un mensaje de prueba.",
            "is_read": False,
            "deleted": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), messages_count + 1)
        response_json = json.loads(response.content)
        self.assertIn('date', response_json)
        self.assertIsNotNone(response_json.pop('date'))
        self.assertEqual(response_json, expected)

    def test_update_message(self):
        url = '/api/messages/1/'
        data = {
            "sender": 1,
            "reciever": 2,
            "event": 2,
            "subject": "Mensaje de prueba",
            "body": "Hola! Este es un mensaje de prueba.",
        }
        expected = {
            "id": 1,
            "sender": 1,
            "reciever": 2,
            "event": 2,
            "subject": "Mensaje de prueba",
            "body": "Hola! Este es un mensaje de prueba.",
            "is_read": True,
            "date": "2022-05-04T12:01:16.446Z",
            "deleted": False
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)
