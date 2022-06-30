from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..models import Movie
from .serializers import MovieSerializer


"""
Its default value is GET
Note: If you do not use this decorator it won't convert your 
python Dictionary into a valid JSON data
"""
@api_view(["GET"])
def movie_list(req: Request) -> Response:
    movies = Movie.objects.all()
    serialized_movies = MovieSerializer(movies, many=True)

    return Response(serialized_movies.data)


@api_view(["GET"])
def movie_details(req: Request, id: int) -> Response:
    movie = Movie.objects.get(pk=id)
    serialized_movie = MovieSerializer(movie)

    return Response(serialized_movie.data)

