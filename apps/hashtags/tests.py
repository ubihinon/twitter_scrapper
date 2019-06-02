from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class HashTagAPITestCase(APITestCase):
    url_name = 'hashtags-tweets'

    def setUp(self):
        self.hashtag = 'python'

    def test_get_list(self):
        response = self.client.get(reverse(self.url_name, [self.hashtag]))
        self.assertEqual(len(response.data), 30)

    def test_get_list_with_limit_less_default(self):
        response = self.client.get(reverse(self.url_name, [self.hashtag]), {'limit': 5})
        self.assertEqual(len(response.data), 5)

    def test_get_list_with_limit_more_default(self):
        response = self.client.get(reverse(self.url_name, [self.hashtag]), {'limit': 50})
        self.assertEqual(len(response.data), 50)
