from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fullname = serializers.CharField(max_length=200)
    href = serializers.CharField(max_length=200)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
