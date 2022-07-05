from typing import NoReturn
from rest_framework.exceptions import NotFound
from django.core.files import File
from django.utils import timezone
from .repositories import MovieRepository
from ..models import Movie
from shared.save_uploaded_file import save_uploaded_file


class MovieService:
    def __init__(self) -> None:
        self.__movie_repository = MovieRepository()
    
    def get_object(self, id: int,):
        try:
            return self.__movie_repository.find_by_id(id)
        except Movie.DoesNotExist:
            raise NotFound(detail='Movie does not exists')
    
    def get_all(self,):
        return self.__movie_repository.find_all()
    
    def upload_file(self, file: File):
        saved_file_name = save_uploaded_file(file)
        # Timezone is really a hard thing to deal. So I decided to keep it in zero timezone
        # Read USE_TZ and generate time based on this setting
        now = timezone.now()
        created_movie = Movie.objects.create(
            name=file.name,
            description=f"File uploaded at {now}",
            active=True,
            file_name=saved_file_name
        )
        return created_movie
    
    """
    Based on onion architecture layer I decided to annotate
    movie with Movie model instead of serializer. Inner layers
    should not dependent to outer layers. Repository/Service layer
    should not be dependent to the View/Controller layer
    """
    def update_movie(self, id: int, movie: Movie,) -> Movie|NoReturn:
        try:
            movie = self.__movie_repository.update_by_id(id, movie)
            return movie
        except Movie.DoesNotExist:
            raise NotFound(detail="Movie not found")
    
    def delete_movie(self, id: int) -> Movie|NoReturn:
        try:
            movie = self.__movie_repository.delete_by_id(id)
            return movie
        
        except Movie.DoesNotExist:
            raise NotFound(detail="Movie not found")

