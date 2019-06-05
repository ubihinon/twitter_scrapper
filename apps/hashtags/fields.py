from rest_framework import serializers


class HashTagField(serializers.ListField):
    child = serializers.CharField(max_length=200)
