from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    id: int = serializers.IntegerField(read_only=True, required=False)
    name: str = serializers.CharField(required=True)
    description: str = serializers.CharField(required=True)
    active: bool = serializers.BooleanField(required=False)

