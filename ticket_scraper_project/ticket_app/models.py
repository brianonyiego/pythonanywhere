# Create your models here.
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    ratings = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.title
