from django.db import models
from apps.events.models import Event
from apps.sales.models import Bill

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    cost = models.IntegerField()
    ubication =  models.CharField(max_length=20)
    state = models.CharField(null=True,max_length=20)
    event = models.name = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)
    id_bill = models.ForeignKey(Bill, null=True, blank=True, on_delete=models.CASCADE)

    def addTicket(self,event):
        tickets = Ticket.objects.get(event=id)
        print (tickets)
        
