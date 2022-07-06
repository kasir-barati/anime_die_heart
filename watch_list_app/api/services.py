import os
import re
import math
import mimetypes
from wsgiref.util import FileWrapper
from typing import NoReturn
from rest_framework.exceptions import NotFound
from django.core.files import File
from django.utils import timezone
from django.http.response import StreamingHttpResponse
from ..utils.range_file_wrapper import RangeFileWrapper
from .repositories import MovieRepository
from ..models import Movie
from ..utils.resize_video import resize_video
from ..utils.save_uploaded_file import prepend_random_string_to_filename
from ..utils.save_uploaded_file import save_uploaded_file
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
        random_filename = self.__generate_random_filename(file.name)
        original_video_absolute_path = os.path.join(
            MEDIA_ROOT, 
            random_filename,
        )
        save_uploaded_file(
            absolute_path=original_video_absolute_path,
            file=file,
        )
        resized_files_absolute_path = self.__resize_video(
            original_video_absolute_path=original_video_absolute_path,
        )

        # Timezone is really a hard thing to deal. So I decided to keep it in zero timezone
        # Read USE_TZ and generate time based on this setting
        now = timezone.now()
        created_movie = Movie.objects.create(
            name=file.name,
            description=f"File uploaded at {now}",
            active=True,
            file_name=original_video_absolute_path,
            resized_files_absolute_path=resized_files_absolute_path
        )

        return created_movie

    def __generate_random_filename(
            self,
            filename: str) -> str:
        random_file_name = prepend_random_string_to_filename(
            filename
        )

        return random_file_name

    def __resize_video(
            self, 
            original_video_absolute_path: str,) -> list[str]:
        base_path = os.path.dirname(
            original_video_absolute_path,
        )
        original_video_size = os.path.getsize(
            original_video_absolute_path,
        )
        filename_with_extension = os.path.basename(
            original_video_absolute_path,
        )
        extension, filename = os.path.splitext(
            filename_with_extension,
        )
        one_third_video_size_filename = \
            self.__generate_random_filename(filename) \
            + 'one_third' \
            + extension
        one_third_video_size_filename = os.path.join(
            base_path,
            one_third_video_size_filename
        )
        resize_video(
            video_absolute_path=original_video_absolute_path,
            output_file_absolute_path=one_third_video_size_filename,
            size_upper_bound=math.ceil(original_video_size/3),
        )

        # Do more converting

        return [one_third_video_size_filename]
    
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

