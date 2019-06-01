from django.conf import settings
from rest_framework import views
from rest_framework.response import Response

from apps.common.serializers import TweetSerializer
from apps.common.tweet_scrapper import TweetScrapper


class UserTweetListView(views.APIView):
    def get(self, request, **kwargs):
        limit = int(request.query_params.get('limit', settings.PAGE_LIMIT))
        user = kwargs.get('user', '')

        tweet_scrapper = TweetScrapper()
        tweets = []

        for tweet in tweet_scrapper.get_user_tweets(user, limit):
            print(tweet)
            tweets.append(tweet)

        return Response(TweetSerializer(tweets, many=True).data)

