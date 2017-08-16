from django.conf import settings

from rest_framework.test import APITestCase

from url_shortener.models import ShortenedURL

class RenderViewTest(APITestCase):

    def setUp(self):
        settings.CELERY_ALWAYS_EAGER = True

    def test_render_http(self):
        original_url = 'http://github.com/erikamsierra'
        db_obj = ShortenedURL(original_url=original_url)
        db_obj.save()

        response = self.client.get(db_obj.shortened_url)
        self.assertEqual(response.status_code, 302)

    def test_render_https(self):
        original_url = 'https://github.com/erikamsierra'
        db_obj = ShortenedURL(original_url=original_url)
        db_obj.save()

        response = self.client.get(db_obj.shortened_url)
        self.assertEqual(response.status_code, 302)

    def test_invalid(self):
        invalid_url = '{}/{}'.format(settings.DOMAIN, 'blaaaaaaa')
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_num_visits(self):
        original_url = 'www.google.com'
        db_obj = ShortenedURL(original_url=original_url)
        db_obj.save()

        self.assertEqual(db_obj.num_visits, 0)

        response = self.client.get(db_obj.shortened_url)
        self.assertEqual(response.status_code, 302)

        db_obj = ShortenedURL.objects.get(original_url=original_url)
        self.assertEqual(db_obj.num_visits, 1)

        response = self.client.get(db_obj.shortened_url)
        self.assertEqual(response.status_code, 302)

        db_obj = ShortenedURL.objects.get(original_url=original_url)
        self.assertEqual(db_obj.num_visits, 2)

    def test_num_visits_no_tracking(self):
        settings.TRACK_VISITS = False

        original_url = 'www.google.com'
        db_obj = ShortenedURL(original_url=original_url)
        db_obj.save()

        self.assertEqual(db_obj.num_visits, 0)

        response = self.client.get(db_obj.shortened_url)
        self.assertEqual(response.status_code, 302)

        db_obj = ShortenedURL.objects.get(original_url=original_url)
        self.assertEqual(db_obj.num_visits, 0)



