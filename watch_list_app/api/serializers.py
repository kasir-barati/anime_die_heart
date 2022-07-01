from rest_framework import serializers
from djongo.models import ObjectIdField
from ..models import MovieFile


class MovieSerializer(serializers.Serializer):
    _id: ObjectIdField = serializers.CharField(read_only=True, required=False)
    name: str = serializers.CharField(required=True)
    description: str = serializers.CharField(required=True)
    active: bool = serializers.BooleanField(required=False)


class UploadMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieFile
        fields = '__all__'
