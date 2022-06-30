from django.db import models

# Create your models here.
class Movie(models.Model):
    name: str = models.CharField(max_length=100, null=False)
    description: str = models.CharField(max_length=400, null=False)
    active: bool = models.BooleanField(default=True)

    def __str__(self):
        return self.name