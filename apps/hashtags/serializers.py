from rest_framework import serializers


class HashTagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
