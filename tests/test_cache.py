from django.core.cache import cache
from django.conf import settings

from rest_framework.test import APITestCase

from url_shortener.models import ShortenedURL

class CacheTest(APITestCase):

    def test_cache_storage_from_post(self):
        original_url = 'https://github.com/erikamsierra'

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 201)

        db_obj = ShortenedURL.objects.get(original_url=original_url)
        self.assertEqual(cache.get(db_obj.short_code), original_url)

        cache.delete(db_obj.short_code)

    def test_cache_storage_from_post_duplicate(self):
        original_url = 'https://github.com/erikamsierra'

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 201)

        db_obj = ShortenedURL.objects.get(original_url=original_url)
        self.assertEqual(cache.get(db_obj.short_code), original_url)

        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 201)

        db_obj = ShortenedURL.objects.get(original_url=original_url)
        self.assertEqual(cache.get(db_obj.short_code), original_url)

        cache.delete(db_obj.short_code)

    def test_cache_storage_from_get(self):
        original_url = 'https://github.com/erikamsierra'

        db_obj = ShortenedURL(original_url=original_url)
        db_obj.save()
        self.assertEqual(cache.get(db_obj.short_code), None)

        response = self.client.get(db_obj.shortened_url)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(cache.get(db_obj.short_code), original_url)

        cache.delete(db_obj.short_code)

    def test_cache_read(self):
        original_url = 'https://github.com/erikamsierra'
        short_code = '1234zXCv'
        shortened_url = '{}/{}'.format(settings.DOMAIN, short_code)

        cache.set(short_code, original_url)

        response = self.client.get(shortened_url)
        # The entry doesn't exist in the db so this would only work if cache is working
        self.assertEqual(response.status_code, 302)

        cache.delete(short_code)


