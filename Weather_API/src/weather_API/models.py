from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    city = models.TextField()
    state = models.TextField()

class weather_data(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(auto_now=False)
    location = models.OneToOneField(Location,on_delete = models.CASCADE)
    temperature = ArrayField(
                            models.FloatField(),
                                    size = 24)