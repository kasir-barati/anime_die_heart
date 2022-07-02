from rest_framework.exceptions import bad_request
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from rest_framework.exceptions import NotFound
from zoneinfo import ZoneInfo
from rest_framework import status
from django.core.files import File
import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request
from ..models import Movie
from .serializers import MovieSerializer
from .serializers import UploadMovieSerializer
"""
IDK but my gut tells me how Python work is at odds with its documentation. 
This is just my Opinion.
Here it says use relative imports: https://peps.python.org/pep-0328/
But here it defines another rule: https://docs.python.org/3.9/tutorial/modules.html#intra-package-references
"""
from shared.save_uploaded_file import save_uploaded_file


"""
Its default value is GET
Note: If you do not use this decorator it won't convert your 
python Dictionary into a valid JSON data
"""
@api_view(["GET"])
def movies_list(req: Request) -> Response:
    movies = Movie.objects.all()
    serialized_movies = MovieSerializer(movies, many=True)

    return Response(serialized_movies.data)


@api_view(["GET"])
def movie_details(req: Request, id: int) -> Response:
    movie = Movie.objects.get(pk=id)

    if movie == None:
        raise NotFound(detail="Movie not found")

    serialized_movie = MovieSerializer(movie)

    return Response(serialized_movie.data)


@api_view(["GET"])
def stream_movie(req: Request, id: int) -> StreamingHttpResponse:
    movie = Movie.objects.get(pk=id)
    
    if movie == None:
        raise NotFound(detail="Movie not found")

    file_binary = open(movie.file_name, "rb")
    converted_iterable_file = FileWrapper(file_binary)
    response = StreamingHttpResponse(converted_iterable_file)

    return response


@api_view(["PATCH"])
def update_created_movie(req: Request, id: int) -> Response:
    serialized_movie = MovieSerializer(req.body)
    movie = Movie.objects.filter(pk=id).update(
        name=serialized_movie.name,
        description=serialized_movie.description,
        active=serialized_movie.active
    )
    
    serialized_movie = MovieSerializer(movie)
    response = Response(serialized_movie.data)

    return response


@api_view(["POST"])
def upload_movie(req: Request) -> Response:
    if 'file' not in req.FILES:
        return bad_request(req, 'Please select a file')

    serialized_movie = UploadMovieSerializer(data=req.data)
    """
    Wrong usage
    <MultiValueDict: {'file': [<InMemoryUploadedFile: Untitled.png (image/png)>]}>
    req.FILES.file
    """
    sent_file: File = req.FILES['file']
    saved_file_name = save_uploaded_file(sent_file)

    # Timezone is really a hard thing to deal. So I decided to keep it in zero timezone
    now = datetime.datetime.now(tz=ZoneInfo("Etc/GMT"))
    created_move = Movie.objects.create(
        name=sent_file.name,
        description=f"File uploaded at {now}",
        active=True,
        file_name=saved_file_name
    )
    created_move.save()

    serialized_movie = MovieSerializer(created_move)
    return Response(
        serialized_movie.data, 
        status=status.HTTP_201_CREATED
    )

