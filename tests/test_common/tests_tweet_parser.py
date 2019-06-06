from bs4 import BeautifulSoup
from django.test import TestCase

from apps.common.tweet_scrapper import TweetParser
from tests.core.base import BaseTestMixin


class TweetParserTests(BaseTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.parser = TweetParser()

    def test_retrieve_tweets(self):
        html = self._get_file_data()

        tweets = self.parser.retrieve_tweets(10, html)
        self.assertEqual(len(tweets), 1)

        tweet = tweets[0]
        self.assertEqual(tweet['account']['id'], 16913772)
        self.assertEqual(tweet['account']['href'], '/VisualStudio')
        self.assertEqual(tweet['account']['fullname'], 'Visual Studio')
        self.assertListEqual(tweet['hashtags'], ['#Python', '#VSCode'])
        self.assertEqual(tweet['date'], '10:08 AM - 31 May 2019')
        self.assertEqual(tweet['likes'], 79)
        self.assertEqual(tweet['replies'], 2)
        self.assertEqual(tweet['retweets'], 35)
        self.assertIn('The May 2019 release of the #Python Extension', tweet['text'])
        self.assertIn('IntelliSense in the Python Interactive Window', tweet['text'])
        self.assertIn('Improvements to the Python Language Server and more', tweet['text'])

    def test_retrieve_item_header_data(self):
        bs_obj = self._get_item_header()

        account = self.parser.retrieve_account(bs_obj)
        date = self.parser.retrieve_date(self._get_item_header())

        self.assertEqual(account['id'], 14159138)
        self.assertEqual(account['href'], '/raymondh')
        self.assertEqual(account['fullname'], 'Raymond Hettinger')
        self.assertEqual(date, '9:31 PM - 30 May 2019')

    def test_retrieve_item_footer_data(self):
        bs_obj = self._get_item_footer()

        replies = self.parser.retrieve_replies_count(bs_obj)
        retweets = self.parser.retrieve_retweets_count(bs_obj)
        likes = self.parser.retrieve_likes_count(bs_obj)

        self.assertEqual(replies, 10)
        self.assertEqual(retweets, 92)
        self.assertEqual(likes, 399)

    def test_retrieve_item_content_data(self):
        bs_obj = self._get_item_content()

        hashtags = self.parser.retrieve_hashtags(bs_obj)
        text = self.parser.retrieve_text(bs_obj)

        self.assertListEqual(hashtags, ['#Python', '#pyser2019'])
        self.assertIn('conference software now with @meka_floss here at #pyser2019', text)
        self.assertIn('pic.twitter.com/5OwHHObJnP', text)

    def _get_file_data(self):
        file = self.open_asset('tweet.html')
        return file.read().decode('utf-8')

    def _get_item_header(self):
        file = self.open_asset('item_header.html')
        html = file.read().decode('utf-8')
        return self._create_beautiful_soup(html)

    def _get_item_footer(self):
        file = self.open_asset('item_footer.html')
        html = file.read().decode('utf-8')
        return self._create_beautiful_soup(html)

    def _get_item_content(self):
        file = self.open_asset('item_content.html')
        html = file.read().decode('utf-8')
        return self._create_beautiful_soup(html)

    @staticmethod
    def _create_beautiful_soup(html):
        return BeautifulSoup(html, 'lxml')
