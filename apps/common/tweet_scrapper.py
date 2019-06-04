import math
import re
import sys
from datetime import datetime
from urllib import parse

import dryscrape
import pytz
from bs4 import BeautifulSoup

PAGE_SIZE = 20


class TweetScrapper:

    def __init__(self, limit) -> None:
        super().__init__()
        self.limit = limit
        self.tweet_parser = TweetParser()
        self.session = None

    def get_tweets_by_tag(self, hashtag):
        encoded_url = parse.urlencode({'q': f'#{hashtag}', 'src': 'typd'})
        url = f'https://twitter.com/search?{encoded_url}'

        html = self.get_body_response(url)
        tweets = self.tweet_parser.retrieve_tweets(self.limit, html)

        return tweets

    def get_user_tweets(self, user):
        url = f'https://twitter.com/{user}'

        html = self.get_body_response(url)
        return self.tweet_parser.retrieve_tweets(self.limit, html)

    def get_body_response(self, url):
        if 'linux' in sys.platform:
            dryscrape.start_xvfb()

        self.session = dryscrape.Session()
        self.session.set_attribute('auto_load_images', False)
        self.session.set_header('User-agent', 'Google Chrome')

        self.session.visit(url)

        for i in range(math.ceil(self.limit / PAGE_SIZE)):
            self._load_more_results()

        return self.session.body()

    def _load_more_results(self):
        self.session.exec_script('window.scrollTo(0, document.body.scrollHeight);')
        self.session.wait_for(self._is_tweets_loaded, timeout=30)

    def _is_tweets_loaded(self):
        initial_count = self._get_tweets_count()
        count = initial_count

        while count < initial_count + 1:
            count = self._get_tweets_count()

        return True

    def _get_tweets_count(self):
        html = self.session.body()
        return self.tweet_parser.get_tweets_count(html)


class TweetParser:
    def retrieve_tweets(self, limit, html):
        parser = BeautifulSoup(html, features='lxml')
        tweets = []

        for tweet in parser.body.find_all('div', attrs={'class': 'tweet'}, limit=limit):
            tweets.append(self.get_tweet(tweet))

        return tweets

    def get_tweet(self, bs_obj):
        return {
            'account': self.retrieve_account(bs_obj),
            'hashtags': self.retrieve_hashtags(bs_obj),
            'date': self.retrieve_date(bs_obj),
            'likes': self.retrieve_likes_count(bs_obj),
            'replies': self.retrieve_replies_count(bs_obj),
            'retweets': self.retrieve_retweets_count(bs_obj),
            'text': self.retrieve_text(bs_obj)
        }

    def retrieve_account(self, bs_obj):
        account_data = bs_obj.find(
            'a',
            attrs={'class': 'account-group'}
        )
        account = {
            'id': int(account_data.get('data-user-id')),
            'href': account_data.get('href'),
            'fullname': account_data.find('strong', attrs={'class': 'fullname'}).text
        }

        return account

    def retrieve_date(self, bs_obj):
        timestamp = int(bs_obj.find('a', attrs={'class': 'tweet-timestamp'}).find('span').get('data-time-ms'))
        # date = datetime.utcfromtimestamp(timestamp / 1000.0).strftime('%-I:%M %p - %-d %b %Y')
        date = datetime.utcfromtimestamp(timestamp / 1000.0)
        aware_utc_dt = date.replace(tzinfo=pytz.utc)

        return aware_utc_dt.strftime('%-I:%M %p - %-d %b %Y')

    def retrieve_likes_count(self, bs_obj):
        return self._retrieve_count_value(bs_obj, 'ProfileTweet-action--favorite u-hiddenVisually')

    def retrieve_replies_count(self, bs_obj):
        return self._retrieve_count_value(bs_obj, 'ProfileTweet-action--reply u-hiddenVisually')

    def retrieve_retweets_count(self, bs_obj):
        return self._retrieve_count_value(bs_obj, 'ProfileTweet-action--retweet u-hiddenVisually')

    def retrieve_hashtags(self, bs_obj):
        containers = bs_obj.find_all('a', attrs={'data-query-source': 'hashtag_click'})
        return [c.text for c in containers]

    def retrieve_text(self, bs_obj):
        return bs_obj.find('p', attrs={'class': 'tweet-text'}).text

    def get_tweets_count(self, html):
        size = len(
            re.findall('<div.+class=\"tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable', html)
        )
        return size

    def _retrieve_count_value(self, bs_obj, container_class_name):
        container = bs_obj.find('span', attrs={'class': container_class_name})
        count = container.find('span', attrs={'class': 'ProfileTweet-actionCount'}).get('data-tweet-stat-count')

        return int(count)
