from django.db import models
from apps.events.models import Event

# Create your models here.
class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    cost = models.IntegerField(null=True)
    event = models.name = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):   #MUESTRA EL NOMBRE COMO LLAVE FORANEA
        return '{}'.format(self.name)