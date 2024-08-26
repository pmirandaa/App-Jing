from rest_framework import status
from rest_framework.test import APITestCase

from News.models import News, NewsCategory


class NewsTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get News instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_news_list(self):
        url = '/api/news/'
        expected = [
            {
                "id": 1,
                "title": "",
                "short_story": "¡Hemos concluido la versión 2020 de los JING! 🎉",
                "date": "2021-12-21T10:29:01.404000-03:00",
                "publisher": 1,
                "body": "¡Hemos concluido la versión 2020 de los JING! 🎉\r\nGracias a las universidades y a los participantes que promovieron un ambiente grato en las competencias.\r\nHa sido toda un aventura este año, pero se logró y fue posible gracias a las personas que dieron todo por hacer posible esto juegos.❤️\r\n¡Nos vemos en la próxima versión! ✌🏻",
                "category": 1,
                "picture": "news/129033318_403015194230336_145316373917594397_n.jpg",
                "event": 1
            }
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_news_instance(self):
        url = '/api/news/1/'
        expected = {
            "id": 1,
            "title": "",
            "short_story": "¡Hemos concluido la versión 2020 de los JING! 🎉",
            "date": "2021-12-21T10:29:01.404000-03:00",
            "publisher": 1,
            "body": "¡Hemos concluido la versión 2020 de los JING! 🎉\r\nGracias a las universidades y a los participantes que promovieron un ambiente grato en las competencias.\r\nHa sido toda un aventura este año, pero se logró y fue posible gracias a las personas que dieron todo por hacer posible esto juegos.❤️\r\n¡Nos vemos en la próxima versión! ✌🏻",
            "category": 1,
            "picture": "news/129033318_403015194230336_145316373917594397_n.jpg",
            "event": 1
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update News
    # ======================

    def test_create_news(self):
        url = '/api/news/'
        news_count = News.objects.count()
        data = {
            "title": "Nueva noticia de prueba",
            "short_story": "Bajada de prueba",
            "publisher": 2,
            "body": "Cuerpo de noticia de prueba",
            "category": 1,
            "picture": "",
            "event": 2
        }
        expected = {
            "id": news_count + 1,
            "title": "Nueva noticia de prueba",
            "short_story": "Bajada de prueba",
            "publisher": 2,
            "body": "Cuerpo de noticia de prueba",
            "category": 1,
            "picture": "",
            "event": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), news_count + 1)
        response_json = json.loads(response.content)
        self.assertIn('date', response_json)
        self.assertIsNotNone(response_json.pop('date'))
        self.assertEqual(response_json, expected)

    def test_update_news(self):
        url = '/api/news/1/'
        data = {
        }
        expected = {
            "id": 1,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)


class NewsCategoryTest(APITestCase):
    fixtures = ['test_fixture.json']

    # Get NewsCategory instance and list
    # =====================

    def setUp(self):
        self.client.login(username='scisneros', password='123')

    def test_get_news_categories_list(self):
        url = '/api/news_categories/'
        expected = [
            {
                "id": 1,
                "name": "Anuncios",
                "icon": "🔔",
                "color": "blue",
                "btn_class": "btn-primary",
                "event": 1
            }
        ]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    def test_get_news_category_instance(self):
        url = '/api/news_categories/1/'
        expected = {
            "id": 1,
            "name": "Anuncios",
            "icon": "🔔",
            "color": "blue",
            "btn_class": "btn-primary",
            "event": 1
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)

    # Create and update NewsCategory
    # ======================

    def test_create_news_category(self):
        url = '/api/news_categories/'
        news_categories_count = NewsCategory.objects.count()
        data = {
            "name": "Convocatoria",
            "icon": "📝",
            "color": "blue",
            "btn_class": "btn-primary",
            "event": 1
        }
        expected = {
            "id": news_categories_count + 1,
            "name": "Convocatoria",
            "icon": "📝",
            "color": "blue",
            "btn_class": "btn-primary",
            "event": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsCategory.objects.count(),
                         news_categories_count + 1)
        self.assertJSONEqual(response.content, expected)

    def test_update_news_category(self):
        url = '/api/news_categories/1/'
        data = {
            "name": "Urgente",
            "icon": "❗",
            "color": "red",
            "btn_class": "btn-secondary",
            "event": 2
        }
        expected = {
            "id": 1,
            "name": "Urgente",
            "icon": "❗",
            "color": "red",
            "btn_class": "btn-secondary",
            "event": 2
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected)
