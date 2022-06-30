from rest_framework.exceptions import bad_request
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
def movie_list(req: Request) -> Response:
    movies = Movie.objects.all()
    serialized_movies = MovieSerializer(movies, many=True)

    return Response(serialized_movies.data)


@api_view(["GET"])
def movie_details(req: Request, id: int) -> Response:
    movie = Movie.objects.get(pk=id)
    serialized_movie = MovieSerializer(movie)

    return Response(serialized_movie.data)


@api_view(["POST"])
def upload_movie(req: Request) -> Response:
    if 'file' not in req.FILES.file:
        return bad_request(req, 'Please select a file')

    serialized_movie = UploadMovieSerializer(data=req.data)
    sent_file: File = req.FILES.file
    save_uploaded_file(sent_file)

    # Timezone is really a hard thing to deal. So I decided to keep it in zero timezone
    now = datetime.datetime.now(tz=ZoneInfo("Etc/GMT"))
    created_move = Movie.objects.create(
        name=sent_file.name,
        description=f"File uploaded at {now}",
        active=True
    )
    created_move.save()

    serialized_movie = MovieSerializer(created_move)
    return Response(
        serialized_movie, 
        status=status.HTTP_201_CREATED
    )

