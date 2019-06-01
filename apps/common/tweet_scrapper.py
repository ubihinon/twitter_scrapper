import sys
from datetime import datetime
from urllib import parse

import dryscrape
from bs4 import BeautifulSoup


class TweetScrapper:
    def get_tweets_by_tag(self, tag, limit):

        encoded_url = parse.urlencode({'q': tag, 'src': 'typd'})
        url = f'https://twitter.com/search?{encoded_url}'

        html = self.get_body_response(url)
        return TweetParser().get_tweets(tag, limit, html)

    def get_body_response(self, url):
        if 'linux' in sys.platform:
            dryscrape.start_xvfb()

        session = dryscrape.Session()
        session.visit(url)

        return session.body()


class TweetParser:
    def get_tweets(self, tag, limit, html):
        parser = BeautifulSoup(html)
        tweets = []

        for tweet in parser.body.find_all('div', attrs={'class': 'tweet'}, limit=limit):
            tweets.append(self.get_tweet(tweet, tag))

        return tweets

    def get_tweet(self, bs_obj, tag):
        return {
            'account': self.get_account(bs_obj),
            'hashtags': [tag],
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
        date = datetime.fromtimestamp(date/1000.0).strftime('%-I:%M %p - %-d %b %Y')
        # return timezone.localtime(date)
        return date

    def get_likes(self, bs_obj):
        return self._get_count_value(bs_obj, 'ProfileTweet-action--favorite')

    def get_replies(self, bs_obj):
        return self._get_count_value(bs_obj, 'ProfileTweet-action--reply')

    def get_retweets(self, bs_obj):
        return self._get_count_value(bs_obj, 'ProfileTweet-action--retweet')

    def get_text(self, bs_obj):
        return bs_obj.find('p', attrs={'class': 'tweet-text'}).text

    def _get_count_value(self, bs_obj, container_class_name):
        container = bs_obj.find('div', attrs={'class': container_class_name})
        count = container.find('span', attrs={'class': 'ProfileTweet-actionCount'}).get('data-tweet-stat-count')

        if not count:
            count = container.find('span', attrs={'class': 'ProfileTweet-actionCountForPresentation'}).text

        return int(count) if count else 0
