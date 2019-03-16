from django.db import models
from ..users.models import Profile, User
from django.utils import timezone

# Create your models here.

class Bill(models.Model):
	id = models.AutoField(primary_key=True)
	id_profile = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE, related_name='my_bills')
	date_bill = models.DateField(default=timezone.now)
	payment_method = models.CharField(null=True,max_length=30)

def __str__(self):   #MUESTRA EL NOMBRE COMO LLAVE FORANEA
    return '{}'.format(self.id)