from django.db import models
from django.db.models.indexes import Index

# Create your models here.
class Movie(models.Model):
    name: str = models.CharField(max_length=100, null=False)
    description: str = models.CharField(max_length=400, null=False)
    active: bool = models.BooleanField(default=True)
    """
    auto_created
    Boolean flag that indicates if the field was automatically created, 
    such as the OneToOneField used by model inheritance.
    auto_now_add
    Automatically set the field to now when the object is first created. 
    Useful for created_at. If you set a value for this field when creating
    the object, it will be ignored. If you want to be able to modify this 
    field, set the following instead of auto_now_add=True:
    created_at = models.DateTimeField(default=timezone.now )
    """
    created_at = models.DateTimeField(auto_now_add=True)
    """
    Automatically set the field to now every time the object is saved. 
    Useful for updated_at.
    """
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ['-created_at']
        db_table: str = 'movies'
        indexes: Index = [
            models.Index(fields=['name'], name='movie_name_index')
        ]
