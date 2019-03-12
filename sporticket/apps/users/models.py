from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
# Create your models here.


class Profile(models.Model):

	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	identification = models.CharField(max_length=20, null=False, blank=False, unique=True)
	userType = models.CharField(max_length=20, null=False)
	phone = models.CharField(max_length=12)
	numAccount = models.CharField(max_length=20)

	def __str__(self):
		return '{}'.format(self.identification)

	class Meta:

		permissions = {
			('Vendedor', _('Vendedor')),
			('Gerente', _('Gerente')),
			('Externo', _('Externo')),
		}

class Seller(models.Model):

		profile = models.OneToOneField(Profile, primary_key=True, on_delete=models.PROTECT)

		def save_data(self, profile):
			newSeller = Seller(profile=profile)
			newSeller.save()



class Manager(models.Model):

		profile = models.OneToOneField(Profile, primary_key=True, on_delete=models.PROTECT)

		def save_data(self):
			newManager = Manager(profile=profile)
			newManager.save()

class Buyer(models.Model):

		profile = models.OneToOneField(Profile, primary_key=True, on_delete=models.PROTECT)

		def save_data(self,profile):
			newBuyer = Buyer(profile=profile)
			newBuyer.save()
			