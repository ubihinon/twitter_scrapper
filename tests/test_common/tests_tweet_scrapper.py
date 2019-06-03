from django.test import TestCase

from apps.common.tweet_scrapper import TweetParser
from tests.core.base import BaseTestMixin


class TweetScrapperTestCase(BaseTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.parser = TweetParser()

    def test_get_tweets(self):
        html = self._get_file_data()
        tweets = self.parser.get_tweets(10, html)

        self.assertEqual(len(tweets), 1)

        tweet = tweets[0]

        self.assertEqual(tweet['account']['id'], 177238201)
        self.assertEqual(tweet['account']['href'], '/mrYateh')
        self.assertEqual(tweet['account']['fullname'], 'Test Fullname')
        self.assertEqual(tweet['hashtags'], [])
        self.assertEqual(tweet['date'], '10:06 AM - 25 Apr 2019')
        self.assertEqual(tweet['likes'], 38431)
        self.assertEqual(tweet['replies'], 233)
        self.assertEqual(tweet['retweets'], 21278)
        self.assertIn('Lorem Ipsum is simply dummy text of the printing and typesetting industry.', tweet['text'])

    def test_get_tweets_count(self):
        html = self._get_file_data()
        self.assertEqual(self.parser.get_tweets_count(html), 1)

    def _get_file_data(self):
        file = self.open_asset('tweet.html')
        return file.read().decode('utf-8')
