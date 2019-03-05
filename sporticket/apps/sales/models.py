from django.db import models
from ..users.models import Profile

# Create your models here.

class Bill(models.Model):
	id = models.AutoField(primary_key=True)
	id_profile = models.ForeignKey(Profile, null=True, blank=False, on_delete=models.CASCADE)
	time_bill = models.TimeField(auto_now=True)
	payment_method = models.CharField(null=True,max_length=30)

def __str__(self):   #MUESTRA EL NOMBRE COMO LLAVE FORANEA
    return '{}'.format(self.id)