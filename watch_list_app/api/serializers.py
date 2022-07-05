from wsgiref.util import request_uri
from rest_framework import serializers
from rest_framework.serializers import FileField
from ..models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """
    This can help but it is require too much work and decrease maintainability 
    """
    # description = serializers.CharField(required=False)
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

