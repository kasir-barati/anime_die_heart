from rest_framework import serializers
from rest_framework.serializers import FileField
from ..models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        read_only_fields = ('id', 'file_name',)
        fields = ['id', 'name', 'description', 'active', 'file_name']

class UploadMovieSerializer(serializers.Serializer):
    file: FileField = serializers.FileField(
        allow_empty_file=False,
        max_length=None,
        required=True
    )

