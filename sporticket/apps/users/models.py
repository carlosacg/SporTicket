from django.db import models

# Create your models here.

class Users(models.Model):
	identification = models.CharField(max_length=50, primary_key=True)
	name = models.CharField(max_length=50)
	lastName = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	userType = models.CharField(max_length=100)
	phone = models.CharField(max_length=12)
	password = models.CharField(max_length=100)
	numAccount = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
