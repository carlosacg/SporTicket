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
    image = models.ImageField(null=True)

    def __str__(self):   #MUESTRA EL NOMBRE COMO LLAVE FORANEA
        return '{}'.format(self.id)

    def lastEventId(self):
        return str(Event.objects.latest('id'))
    
    def cancelEvent(self,id):
        event = Event.objects.get(id=id)
        event.state = 'Cancelado'
        event.save()
    
    def activateEvent(self,id):
        event = Event.objects.get(id=id)
        event.state = 'Activo'
        event.save()
    
    def save_data(self,name,initial_date,initial_time,place,url,state,capacity,visitor,local,event_type):
        newEvent = Event(name=name,initial_date=initial_date,initial_time=initial_time,place=place,url=url,state=state,capacity=capacity,visitor=visitor,local=local,event_type=event_type)
        newEvent.save()


class Document(models.Model):
    filename = models.CharField(max_length=100)
    docfile = models.FileField(upload_to='documents/')
    
    def __unicode__(self):
         return '%s' % (self.nombre)

class Image(models.Model):
    filename = models.CharField(max_length=100)
    docfile = models.ImageField(upload_to='static/images/')
    
    def __unicode__(self):
         return '%s' % (self.nombre)

