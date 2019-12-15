import json
from django.db import models

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
    temperature = models.TextField(default='[]')

    @property
    def list(self):
        return json.loads(self._list)

    @list.setter
    def list(self, value):
        print(value)
        self._list = json.dumps(self.list + value)

