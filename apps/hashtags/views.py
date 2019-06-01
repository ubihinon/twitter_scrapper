import sys

import dryscrape as dryscrape
from bs4 import BeautifulSoup
from rest_framework import views
from rest_framework.response import Response

from apps.common.serializers import TweetSerializer

PAGE_LIMIT = 30


class TweetScrapper:
    def get_tweets_by_tag(self, tag, limit):
        url = f'https://twitter.com/search?q={tag}&src=typd'

        html = self.get_body_response(url)
        return self.get_tweets(limit, html)

    def get_tweets(self, limit, html):
        parser = BeautifulSoup(html)
        tweets = []

        for tweet in parser.body.find_all('div', attrs={'class': 'tweet'}, limit=limit):
            tweets.append(self.get_tweet(tweet))

        return tweets

    def get_tweet(self, bs_obj):
        return {
            'account': self.get_account(bs_obj),
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
        return int(bs_obj.find('a', attrs={'class': 'tweet-timestamp'}).find('span').get('data-time-ms'))

    def get_likes(self, bs_bj):
        return bs_bj.find('div', attrs={
            'class': 'ProfileTweet-action--favorite'})\
            .find('span', attrs={'class': 'ProfileTweet-actionCountForPresentation'}).text

    def get_replies(self, bs_obj):
        return bs_obj.find('div', attrs={'class': 'ProfileTweet-action--reply'})\
            .find('span', attrs={'class': 'ProfileTweet-actionCountForPresentation'}).text

    def get_retweets(self, bs_obj):
        return bs_obj.find('div', attrs={'class': 'ProfileTweet-action--retweet'})\
            .find('span', attrs={'class': 'ProfileTweet-actionCountForPresentation'}).text

    def get_text(self, bs_obj):
        return bs_obj.find('p', attrs={'class': 'tweet-text'}).text

    def get_body_response(self, url):
        if 'linux' in sys.platform:
            dryscrape.start_xvfb()

        session = dryscrape.Session()
        session.visit(url)

        return session.body()


class TweetListView(views.APIView):
    def get(self, request, **kwargs):
        limit = int(request.query_params.get('limit', PAGE_LIMIT))
        tag = kwargs.get('tag', '')

        tweet_scrapper = TweetScrapper()
        tweets = []
        for tweet in tweet_scrapper.get_tweets_by_tag(tag, limit):
            print(tweet)
            # tweet_serializer = TweetSerializer(data=tweet)
            # tweet_serializer.is_valid(raise_exception=True)
            # tweets.append(tweet_serializer.data)
        # tweet_serializer = TweetSerializer(data={
        #     'account': account,
        #     'hashtags': [],
        #     'date': datetime.fromtimestamp(date/1000.0),
        #     'likes': likes,
        #     'replies': replies,
        #     'retweets': int(retweets),
        #     'text': text
        # })
        # tweet_serializer.is_valid(raise_exception=True)

        return Response(TweetSerializer(tweets, many=True).data)
