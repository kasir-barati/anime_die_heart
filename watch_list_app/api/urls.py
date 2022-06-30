from django.urls import path
from .views import movie_list
from .views import movie_details

urlpatterns = [
    path('', movie_list),
    path('<int:id>', movie_details)
]