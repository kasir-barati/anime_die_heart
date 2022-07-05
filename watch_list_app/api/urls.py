from django.urls import path
from .views import UploadMovie
from .views import GetUpdateDeleteWatchList
from .views import WatchList


urlpatterns = [
    # BUG: You cannot do this in the function based view. more info in those links
    path('', WatchList.as_view(), name='movies-list'),
    path(
        '<int:id>', 
        GetUpdateDeleteWatchList.as_view(), 
        name='get-update-delete-movies-list'
    ),
    path('upload', UploadMovie.as_view()),
    # path('stream', stream_movie)
]

