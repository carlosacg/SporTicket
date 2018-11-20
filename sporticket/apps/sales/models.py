from django.db import models
from ..users.models import Profile

# Create your models here.

class Bill(models.Model):
	id_profile = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE)
	time_bill = models.TimeField(auto_now=True)
