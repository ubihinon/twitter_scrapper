from django.conf import settings
from rest_framework import views
from rest_framework.response import Response

from apps.common.serializers import TweetSerializer
from apps.common.tweet_scrapper import TweetScrapper


class TweetListByHashtagView(views.APIView):
    def get(self, request, **kwargs):
        limit = int(request.query_params.get('limit', settings.PAGE_LIMIT))
        tag = kwargs.get('tag', '')

        tweet_scrapper = TweetScrapper(limit)
        tweets = []

        for tweet in tweet_scrapper.get_tweets_by_tag(tag):
            tweets.append(tweet)

        return Response(TweetSerializer(tweets, many=True).data)
