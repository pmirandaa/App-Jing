from rest_framework import status
from rest_framework.test import APITestCase

from University.models import University


class UniversityTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get University instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_universities_list(self):
        url = '/api/universities/'
        expected = [
            {
                "id": 1,
                "name": "Universidad de Chile",
                "city": "Santiago",
                "logo": None,
                "map": None,
                "short_name": "UCH"
            },
            {
                "id": 2,
                "name": "Universidad Católica",
                "city": "Santiago",
               "logo": None,
                "map": None,
                "short_name": "PUC"
            },
            {
                "id": 3,
                "name": "Universidad de Concepción",
                "city": "Concepción",
                "logo": None,
                "map": None,
                "short_name": "UdeC"
            },
            {
                "id": 4,
                "name": "Universidad de Valparaíso",
                "city": "Valparaíso",
                "logo": None,
                "map": None,
                "short_name": "UV"
            },
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_university_instance(self):
        url = '/api/universities/1/'
        expected = {
            "id": 1,
            "name": "Universidad de Chile",
            "city": "Santiago",
            "logo": None,
            "map": None,
            "short_name": "UCH"
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update University
    # ======================

    def test_create_university(self):
        url = '/api/universities/'
        universities_count = University.objects.count()
        data = {
            "name": "Universidad Técnica Federico Santa María",
            "city": "Valparaíso",
            "short_name": "USM"
        }
        expected = {
            "id": universities_count + 1,
            "name": "Universidad Técnica Federico Santa María",
            "city": "Valparaíso",
            "logo": None,
            "map": None,
            "short_name": "USM"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(University.objects.count(), universities_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_university(self):
        url = '/api/universities/1'
        data = {
            "name": "Universidad de Talca",
            "city": "Talca",
            # TODO: Update logo and map
            "short_name": "UTalca"
        }
        expected = {
            "id": 1,
            "name": "Universidad de Talca",
            "city": "Talca",
            "logo": None,
            "map": None,
            "short_name": "UTalca"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)
