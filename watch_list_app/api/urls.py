from django.urls import path
from .views import movie_list
from .views import movie_details
from .views import upload_movie

urlpatterns = [
    path('', movie_list),
    path('<int:id>', movie_details),
    path('upload', upload_movie)
]