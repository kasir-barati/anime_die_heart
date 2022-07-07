import os
import re
import mimetypes
from wsgiref.util import FileWrapper
from typing import NoReturn
from rest_framework.exceptions import NotFound
from django.core.files import File
from django.utils import timezone
from django.core.files import File
from django.http.response import StreamingHttpResponse
from .tasks import celery_resize_file
from ..utils.range_file_wrapper import RangeFileWrapper
from ..utils.save_uploaded_file import save_uploaded_file
from .repositories import MovieRepository
from ..models import Movie
from ..utils.save_uploaded_file import random_filename
from anime_die_heart.settings import MEDIA_ROOT


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
        filename = random_filename(file.name)
        original_video_abs_path = os.path.join(
            MEDIA_ROOT, 
            filename,
        )
        save_uploaded_file(
            absolute_path=original_video_abs_path,
            file=file,
        )
        resized_filename = random_filename(
            file.name,
            'one_third'
        )
        resized_file_absolute_path = os.path.join(
            MEDIA_ROOT, 
            resized_filename,
        )
        celery_resize_file.apply_async([
            original_video_abs_path,
            resized_file_absolute_path,
            3,
        ])

        # Timezone is really a hard thing to deal. So I decided to keep it in zero timezone
        # Read USE_TZ and generate time based on this setting
        now = timezone.now()
        created_movie = Movie.objects.create(
            name=file.name,
            description=f"File uploaded at {now}",
            active=True,
            file_name=original_video_abs_path,
            resized_files_absolute_path=[resized_file_absolute_path]
        )

        return created_movie
    
    """
    Based on onion architecture layer I decided to annotate
    movie with Movie model instead of serializer. Inner layers
    should not dependent to outer layers. Repository/Service layer
    should not be dependent to the View/Controller layer

    TODO: find a way to annotate "movie" automatically
    FIXME: Return updated record
    """
    def update_movie(self, id: int, movie,) -> None|NoReturn:
        try:
            self.__movie_repository.update_by_id(id, movie)
            return
        except Movie.DoesNotExist:
            raise NotFound(detail="Movie not found")
    
    def delete_movie(self, id: int) -> int|NoReturn:
        try:
            self.__movie_repository.delete_by_id(id)
            # TODO: delete the movie from file system too

            return id

        except Movie.DoesNotExist:
            raise NotFound(detail="Movie not found")

    def stream_video(
            self, 
            range_header: str, 
            path: str) -> StreamingHttpResponse:
        range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
        range_match = range_re.match(range_header)
        size: int = os.path.getsize(path)
        content_type, encoding = mimetypes.guess_type(path)
        content_type = content_type or 'application/octet-stream'

        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = int(last_byte) if last_byte else size - 1
            if last_byte >= size:
                last_byte = size - 1
            length = last_byte - first_byte + 1
            response = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
            response['Content-Length'] = str(length)
            response['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        else:
            response = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
            response['Content-Length'] = str(size)

        response['Accept-Ranges'] = 'bytes'
        return response

