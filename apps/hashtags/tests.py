from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class HashTagAPITestCase(APITestCase):
    def test_get_tweets_by_hashtag(self):
        response = self.client.get(reverse('hashtags-tweets', {'tag': 'python'}))
        self.assertEqual(len(response.data), 30)
