import math
import sys
from urllib import parse

import dryscrape

from apps.common.tweet_parser import TweetParser

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

        for i in range(1, math.ceil(self.limit / PAGE_SIZE)):
            self._load_more_results()

        return self.session.body()

    def _load_more_results(self):
        self.session.exec_script('window.scrollTo(0, document.body.scrollHeight);')
        self.session.wait_for(self._is_tweets_loaded, timeout=20)

    def _is_tweets_loaded(self):
        initial_count = self._get_tweets_count()
        if not initial_count:
            return True

        count = self._get_tweets_count()

        while count < initial_count + 1:
            count = self._get_tweets_count()
            if count >= self.limit or self._is_last_tweet():
                break

        return True

    def _get_tweets_count(self):
        return len(self.session.xpath('//*[@class="stream-item-header"]'))

    def _is_last_tweet(self):
        return self._get_tweets_count() % PAGE_SIZE > 0
