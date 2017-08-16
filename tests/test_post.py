import json

from rest_framework.test import APITestCase

from url_shortener.models import ShortenedURL

class ShortenViewSetTest(APITestCase):

    def test_create_no_protocol(self):
        original_url = 'www.google.com'

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 201)

        shortened_url = json.loads(response.content)
        stored_url = "http://{}".format(original_url)
        self.assertEqual(shortened_url['url'], stored_url)
        self.assertTrue(shortened_url['shortened_url'])

        db_obj = ShortenedURL.objects.get(original_url=stored_url)
        self.assertEqual(shortened_url['shortened_url'], db_obj.shortened_url)

    def test_create_https_protocol(self):
        original_url = 'https://github.com/erikamsierra'

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 201)

        shortened_url = json.loads(response.content)
        self.assertEqual(shortened_url['url'], original_url)
        self.assertTrue(shortened_url['shortened_url'])

        db_obj = ShortenedURL.objects.get(original_url=original_url)
        self.assertEqual(shortened_url['shortened_url'], db_obj.shortened_url)

    def test_create_http_protocol(self):
        original_url = 'http://github.com/erikamsierra'

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 201)

        shortened_url = json.loads(response.content)
        self.assertEqual(shortened_url['url'], original_url)
        self.assertTrue(shortened_url['shortened_url'])

        db_obj = ShortenedURL.objects.get(original_url=original_url)
        self.assertEqual(shortened_url['shortened_url'], db_obj.shortened_url)

    def test_create_existing(self):
        original_url = 'http://github.com/erikamsierra'
        data = {'url': original_url}

        # First POST
        response = self.client.post('/shorten_url/', data, format='json')
        shortened_url = json.loads(response.content)
        first_url = shortened_url['shortened_url']

        # Second POST
        response = self.client.post('/shorten_url/', data, format='json')
        shortened_url = json.loads(response.content)
        second_url = shortened_url['shortened_url']

        self.assertEqual(first_url, second_url)

    def test_create_long_url(self):
        original_url = "https://www.google.co.uk/search?q=thai%20restaurant%20london%20stratford&oq=thai+restaurant+london+stratdord&aqs=chrome..69i57j0l2.11755j1j4&sourceid=chrome&ie=UTF-8&npsic=0&rflfq=1&rlha=0&rllag=51544253,-1935,497&tbm=lcl&rldimm=4829868904143521214&ved=0ahUKEwithL-E2NvVAhVlIcAKHcsaBY8QvS4ITjAA&rldoc=1&tbs=lrf:!2m4!1e17!4m2!17m1!1e2!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:9"

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 201)

        shortened_url = json.loads(response.content)
        self.assertEqual(shortened_url['url'], original_url)
        self.assertTrue(shortened_url['shortened_url'])

        db_obj = ShortenedURL.objects.get(original_url=original_url)
        self.assertEqual(shortened_url['shortened_url'], db_obj.shortened_url)

    def test_create_special_chars(self):
        original_url = "http://españa.com"

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 201)

        shortened_url = json.loads(response.content)
        self.assertEqual(shortened_url['url'], original_url)
        self.assertTrue(shortened_url['shortened_url'])

        db_obj = ShortenedURL.objects.get(original_url=original_url)
        self.assertEqual(shortened_url['shortened_url'], db_obj.shortened_url)

    def test_invalid_ftp_protocol(self):
        original_url = 'ftp://ftp.test/test/test.txt'

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 400)

        errors = json.loads(response.content)
        self.assertEqual(errors['url'][0], "Enter a valid URL.")

    def test_missing_url(self):
        data = {}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 400)

        errors = json.loads(response.content)
        self.assertEqual(errors['url'][0], "This field is required.")

    def test_empty_url(self):
        data = {'url': None}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 400)

        errors = json.loads(response.content)
        self.assertEqual(errors['url'][0], "This field may not be null.")

    def test_invalid_url_1(self):
        original_url = 'a'

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 400)

        errors = json.loads(response.content)
        self.assertEqual(errors['url'][0], "Enter a valid URL.")

    def test_invalid_url_2(self):
        original_url = 'a.a'

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 400)

        errors = json.loads(response.content)
        self.assertEqual(errors['url'][0], "Enter a valid URL.")

    def test_invalid_url_3(self):
        original_url = 'google'

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 400)

        errors = json.loads(response.content)
        self.assertEqual(errors['url'][0], "Enter a valid URL.")

    def test_invalid_url_4(self):
        original_url = 'google.'

        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 400)

        errors = json.loads(response.content)
        self.assertEqual(errors['url'][0], "Enter a valid URL.")
