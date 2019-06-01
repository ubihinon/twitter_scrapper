from rest_framework import views
from rest_framework.response import Response

from apps.common.tweet_scrapper import TweetScrapper

PAGE_LIMIT = 30


class TweetListByHashtagView(views.APIView):
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
            tweets.append(tweet)
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

        # return Response(TweetSerializer(tweets, many=True).data)
        return Response(tweets)
