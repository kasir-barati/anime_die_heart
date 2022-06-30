from rest_framework import serializers
from rest_framework.serializers import FileField


class MovieSerializer(serializers.Serializer):
    id: int = serializers.IntegerField(read_only=True, required=False)
    name: str = serializers.CharField(required=True)
    description: str = serializers.CharField(required=True)
    active: bool = serializers.BooleanField(required=False)


class UploadMovieSerializer(serializers.Serializer):
    file: FileField = serializers.FileField(
        allow_empty_file=False,
        max_length=None
    )