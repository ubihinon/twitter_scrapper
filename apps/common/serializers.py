from rest_framework import serializers

from apps.hashtags.fields import HashTagField
from apps.users.serializers import AccountSerializer


# TODO CHECK
class TweetSerializer(serializers.Serializer):
    account = AccountSerializer()
    hashtags = HashTagField()
    date = serializers.DateTimeField(format='%-I:%M %p - %-d %b %Y', input_formats=['%I:%M %p - %d %b %Y'])
    likes = serializers.IntegerField()
    replies = serializers.IntegerField()
    retweets = serializers.IntegerField()
    text = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
