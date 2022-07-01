from djongo.storage import GridFSStorage
from djongo import models
from djongo.models import  FileField
from djongo.models import  ObjectIdField
import anime_die_heart.settings as settings

grid_fs_storage = GridFSStorage(
    collection='myfiles', 
    base_url=''.join([settings.BASE_URL, 'myfiles/'])
)


# Create your models here.
class Movie(models.Model):
    _id: ObjectIdField = models.ObjectIdField()
    name: str = models.CharField(max_length=100, null=False)
    description: str = models.CharField(max_length=400, null=False)
    active: bool = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MovieFile(models.Model):
    _id: ObjectIdField = models.ObjectIdField()
    file: FileField = models.FileField(upload_to='animes', storage=grid_fs_storage)

