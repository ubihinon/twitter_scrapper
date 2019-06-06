from rest_framework import serializers


class HashTagsField(serializers.ListField):
    child = serializers.CharField(max_length=200)
