from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from .serializers import MovieSerializer
from .serializers import UploadMovieSerializer
from .services import MovieService


class WatchList(APIView):
    def __init__(self) -> None:
        super().__init__()
        self.__movie_service = MovieService()

    def get(self, req: Request, format=None) -> Response:
        movies = self.__movie_service.get_all()
        serialized_movies = MovieSerializer(movies, many=True)

        return Response(serialized_movies.data)


class GetUpdateDeleteWatchList(APIView):
    def __init__(self) -> None:
        super().__init__()
        self.__movie_service = MovieService()


    """
    Wrong usage:
    ======================1=======================
    No result even due data is in database

    movie = self.__movie_service.get_object(id)
    serialized_movie = MovieSerializer(data=movie)
    serialized_movie.is_valid()
    =======================2=======================
    AssertionError: Cannot call `.is_valid()` as no `data=` keyword argument was passed when instantiating the serializer instance.

    movie = self.__movie_service.get_object(id)
    serialized_movie = MovieSerializer(movie)
    serialized_movie.is_valid()
    """
    def get(self, req: Request, id: int,):
        movie = self.__movie_service.get_object(id)
        serialized_movie = MovieSerializer(movie)

        return Response(serialized_movie.data)
    
    def patch(self, req: Request, id: int,):
        """
        I could not use same serializer for update. I tried:
            - MovieSerializer(data=req.data, required=False)
            - MovieSerializer(data=req.data)
        """
        serialized_request_body = MovieSerializer(data=req.data, partial=True)
        serialized_request_body.is_valid(raise_exception=True)
        movie = self.__movie_service.update_movie(
            id, 
            serialized_request_body.data
        )

        serialized_movie = MovieSerializer(movie)
        return Response(serialized_movie.data)
    
    def delete(self, req: Request, id: int):
        movie = self.__movie_service.delete_movie(id)

        return Response({"id": id})


class UploadMovie(APIView):
    def __init__(self) -> None:
        super().__init__()
        self.__movie_service = MovieService()

    def post(self, req: Request):
        serialized_movie = UploadMovieSerializer(data=req.data)
        serialized_movie.is_valid(raise_exception=True)
        """
        Wrong usage
        <MultiValueDict: {'file': [<InMemoryUploadedFile: Untitled.png (image/png)>]}>
        req.FILES.file
        """

        sent_file: File = req.data['file']
        created_movie = self.__movie_service.upload_file(sent_file)

        serialized_movie = MovieSerializer(created_movie)
        return Response(
            serialized_movie.data, 
            status=status.HTTP_201_CREATED
        )

