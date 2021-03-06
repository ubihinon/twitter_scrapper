from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class UserTweetsAPITests(APITestCase):
    url_name = 'user-tweets'

    def setUp(self):
        self.username = 'Twitter'

    def test_retrieve_list(self):
        response = self.client.get(reverse(self.url_name, [self.username]))
        self.assertEqual(len(response.data), 30)

    def test_retrieve_list_with_limit_less_default(self):
        response = self.client.get(reverse(self.url_name, [self.username]), {'limit': 5})
        self.assertEqual(len(response.data), 5)

    def test_retrieve_list_with_limit_more_default(self):
        response = self.client.get(reverse(self.url_name, [self.username]), {'limit': 50})
        self.assertEqual(len(response.data), 50)

    def test_username_not_found(self):
        self.username = 'testtesttesttesttesttest1234567890'
        response = self.client.get(reverse(self.url_name, [self.username]), {'limit': 50})
        self.assertEqual(len(response.data), 0)
