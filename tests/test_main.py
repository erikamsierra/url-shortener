import json

from rest_framework.test import APITestCase


class WholeFlowTest(APITestCase):

    def test_redirect_protocol(self):
        original_url = 'https://github.com/erikamsierra'

        # Test POST
        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 201)
        shortened_url = json.loads(response.content)
        self.assertEqual(shortened_url['url'], original_url)
        self.assertTrue(shortened_url['shortened_url'])

        # Test GET
        shortened_url = json.loads(response.content)
        response2 = self.client.get(shortened_url['shortened_url'])
        self.assertEqual(response2.status_code, 302)

    def test_redirect_no_protocol(self):
        original_url = 'www.google.com'
        stored_url = "http://{}".format(original_url)

        # Test POST
        data = {'url': original_url}
        response = self.client.post('/shorten_url/', data, format='json')
        self.assertEqual(response.status_code, 201)
        shortened_url = json.loads(response.content)
        self.assertEqual(shortened_url['url'], stored_url)
        self.assertTrue(shortened_url['shortened_url'])

        # Test GET
        shortened_url = json.loads(response.content)
        response2 = self.client.get(shortened_url['shortened_url'])
        self.assertEqual(response2.status_code, 302)
