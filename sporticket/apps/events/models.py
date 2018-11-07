from django.db import models
import psycopg2

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

    def connect(self): #CONEXION ALTERNATIVA PARA DAR INSTRUCCIONES A LA BD SIN NECESIDAD DE UN FORM
        conn = psycopg2.connect(" \
            dbname=sport_db \
            user=andres \
            password=12345")
        return conn
    
    def cancelEvent(self,id):
        object = Event()
        conn = object.connect()
        cursor = conn.cursor()
        instruction = "UPDATE events_event SET state=\'Cancelado\' WHERE id="+id+";"
        cursor.execute(instruction)
        conn.commit()
        conn.close()

    def save_data(self,name,initial_date,initial_time,place,url,state,capacity,visitor,local,event_type):
        object = Event()
        conn = object.connect()
        cursor = conn.cursor()
        instruction = "INSERT INTO events_event VALUES (nextval(\'events_event_id_seq\'),\'"+name+"\',\'"+initial_date+"\',\'"+initial_time+"\',\'"+place+"\',\'"+url+"\',\'"+state+"\',"+str(capacity)+",\'"+visitor+"\',\'"+local+"\',\'"+event_type+"\');"
        cursor.execute(instruction)
        conn.commit()
        conn.close()

    def insertTickets(self,quantity,ubication,event,cost,state):
        object = Event()
        x=0
        while x < int(quantity):        
            object.save_ticket(ubication,event,cost,state) 
            x+=1    
    
    def save_ticket(self,ubication,event,cost,state):
        object = Event()
        conn = object.connect()
        cursor = conn.cursor()
        instruction = "INSERT INTO tickets_ticket VALUES (nextval(\'tickets_ticket_id_seq\'),"+str(cost)+",\'"+ubication+"\',"+str(event)+",\'"+state+"\');"
        print (instruction)
        cursor.execute(instruction)
        conn.commit()
        print ("GENERO TICKET")
        conn.close()

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

