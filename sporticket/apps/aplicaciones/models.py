from django.db import models

# Create your models here.
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    initial_date = models.DateField()
    initial_time = models.TimeField()
    place = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    capacity = models.IntegerField()
    visitor = models.CharField(max_length=200)
    local = models.CharField(max_length=200)
    event_type = models.CharField(max_length=200)
    
    def __str__(self):   #MUESTRA EL NOMBRE COMO LLAVE FORANEA
        return '{}'.format(self.name)