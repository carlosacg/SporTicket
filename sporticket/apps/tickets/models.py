from django.db import models
from apps.events.models import Event
from apps.sales.models import Bill
from apps.location.models import Location

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(null=True,max_length=20)
    event = models.name = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)
    location = models.name = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)
    id_bill = models.ForeignKey(Bill, null=True, blank=True, on_delete=models.CASCADE)

        
