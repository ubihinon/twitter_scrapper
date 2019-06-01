from rest_framework import serializers

from apps.hashtags.serializers import HashTagSerializer
from apps.users.serializers import AccountSerializer


class TweetSerializer(serializers.Serializer):
    account = AccountSerializer()
    # hashtags = HashTagSerializer(many=True)
    hashtags = serializers.ListField()
    date = serializers.DateTimeField()
    likes = serializers.IntegerField()
    replies = serializers.IntegerField()
    retweets = serializers.IntegerField()
    text = serializers.TimeField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
