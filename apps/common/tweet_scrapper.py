import math
import re
import sys
import time
from datetime import datetime
from functools import partial
from time import sleep
from urllib import parse

import dryscrape
from bs4 import BeautifulSoup

PAGE_SIZE = 20


class TweetScrapper:

    def __init__(self, limit) -> None:
        super().__init__()
        self.limit = limit

    def get_tweets_by_tag(self, tag):
        encoded_url = parse.urlencode({'q': tag, 'src': 'typd'})
        url = f'https://twitter.com/search?{encoded_url}'

        html = self.get_body_response(url)
        tweets = TweetParser().get_tweets(self.limit, html)

        return tweets

    def get_user_tweets(self, user):
        url = f'https://twitter.com/{user}'

        html = self.get_body_response(url)
        return TweetParser().get_tweets(self.limit, html)

    def get_body_response(self, url):
        if 'linux' in sys.platform:
            dryscrape.start_xvfb()

        self.session = dryscrape.Session()
        self.session.set_attribute('auto_load_images', False)
        self.session.set_header('User-agent', 'Google Chrome')

        self.session.visit(url)

        start_time = time.time()
        for i in range(math.ceil(self.limit / PAGE_SIZE)):
            self.load_more_results()
        print(f'Duration time: {time.time() - start_time}')
        return self.session.body()

    def load_more_results(self):
        html = self.session.body()

        self.session.exec_script('window.scrollTo(0, document.body.scrollHeight);')

        self.session.wait_for(partial(self.is_true, TweetParser().get_tweets_count(html)), timeout=30)

    def is_true(self, initial_count):
        # sleep(2)
        # return True
        html = self.session.body()
        count = TweetParser().get_tweets_count(html)
        while count < initial_count + PAGE_SIZE - 5:
            html = self.session.body()
            count = TweetParser().get_tweets_count(html)
        return True


class TweetParser:
    def get_tweets(self, limit, html):
        parser = BeautifulSoup(html)
        tweets = []

        for tweet in self.get_all_tweets(parser, limit):
            tweets.append(self.get_tweet(tweet))

        return tweets

    def get_tweets_count(self, html):
        parser = BeautifulSoup(html)
        size = len(self.get_all_tweets(parser))
        # size = len(re.findall('<div.+class=\"tweet', html))
        return size

    def get_all_tweets(self, bs_obj, limit=None):
        return bs_obj.body.find_all('div', attrs={'class': 'tweet'}, limit=limit)

    def get_tweet(self, bs_obj):
        return {
            'account': self.get_account(bs_obj),
            'hashtags': self.get_hashtags(bs_obj),
            'date': self.get_date(bs_obj),
            'likes': self.get_likes(bs_obj),
            'replies': self.get_replies(bs_obj),
            'retweets': self.get_retweets(bs_obj),
            'text': self.get_text(bs_obj)
        }

    def get_account(self, bs_obj):
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

    def get_date(self, bs_obj):
        date = int(bs_obj.find('a', attrs={'class': 'tweet-timestamp'}).find('span').get('data-time-ms'))
        # return datetime.fromtimestamp(date/1000.0, tz=get_current_timezone())
        # return datetime.fromtimestamp(date/1000.0).strftime('%-I:%M %p - %-d %b %Y')
        date = datetime.fromtimestamp(date / 1000.0).strftime('%-I:%M %p - %-d %b %Y')
        # return timezone.localtime(date)
        return date

    def get_likes(self, bs_obj):
        return self._get_count_value(bs_obj, 'ProfileTweet-action--favorite')

    def get_replies(self, bs_obj):
        return self._get_count_value(bs_obj, 'ProfileTweet-action--reply')

    def get_retweets(self, bs_obj):
        return self._get_count_value(bs_obj, 'ProfileTweet-action--retweet')

    def get_hashtags(self, bs_obj):
        hashtags = []

        containers = bs_obj.find_all('a', attrs={'data-query-source': 'hashtag_click'})

        for container in containers:
            if not container.find('b').findChild():
                hashtags.append(container.text)
            else:
                hashtags.append(container.find('b').findChild().text)

        return hashtags

    def get_text(self, bs_obj):
        return bs_obj.find('p', attrs={'class': 'tweet-text'}).text

    def _get_count_value(self, bs_obj, container_class_name):
        container = bs_obj.find('div', attrs={'class': container_class_name})
        count = container.find('span', attrs={'class': 'ProfileTweet-actionCount'}).get('data-tweet-stat-count')

        if not count:
            count = container.find('span', attrs={'class': 'ProfileTweet-actionCountForPresentation'}).text

        return int(count) if count else 0
