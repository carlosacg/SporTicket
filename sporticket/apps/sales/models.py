from django.db import models
from ..users.models import Profile, User
from ..location.models import Location
from django.utils import timezone

# Create your models here.

class Bill(models.Model):
	id = models.AutoField(primary_key=True)
	id_profile = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE, related_name='my_bills')
	date_bill = models.DateField(default=timezone.now)
	payment_method = models.CharField(null=True,max_length=30)
	type_bill = models.CharField(null=True,max_length=30)
	total_bill = models.BigIntegerField(null=True)

def __str__(self):   #MUESTRA EL NOMBRE COMO LLAVE FORANEA
    return '{}'.format(self.id)

class detailsBill(models.Model):
	id = models.AutoField(primary_key=True)
	id_bill = models.ForeignKey(Bill, null=False, blank=False, on_delete=models.CASCADE)
	id_location = models.ForeignKey(Location, null=False, blank=False, on_delete=models.CASCADE)
	eventName = models.CharField(max_length=50)
	cant = models.IntegerField()
	subtotal = models.IntegerField()
