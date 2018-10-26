from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):

	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	identification = models.CharField(max_length=20, null=False, blank=False)
	userType = models.CharField(max_length=20, null=False)
	phone = models.CharField(max_length=12)
	numAccount = models.CharField(max_length=20)

	def __str__(self):
		return '{}'.format(self.identification)