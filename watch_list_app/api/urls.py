from django.urls import path
from .views import movies_list
from .views import movie_details
from .views import upload_movie
from .views import stream_movie
from .views import update_created_movie

"""
https://github.com/yogeshojha/rengine/blob/master/web/scanEngine/urls.py#L15-L22
https://stackoverflow.com/questions/51574201
https://stackoverflow.com/questions/46156323
https://stackoverflow.com/questions/37054793
https://stackoverflow.com/questions/47360013
https://discord.com/channels/856567261900832808/857642262162964510/992674164244762624
https://discord.com/channels/238666723824238602/308729304949194752/992674927482241024
https://discord.com/channels/222721769696526337/227520285304291329/992682115089059920
https://discord.com/channels/686069011481362462/834654239049384036/992682698281852969
"""

urlpatterns = [
    path('', movies_list, name='movies-list'),
    # BUG: You cannot do this in the function based view. more info in those links
    path('<int:id>', update_created_movie, name='update-created-movie'),
    path('<int:id>', movie_details),
    path('upload', upload_movie),
    path('stream', stream_movie)
]