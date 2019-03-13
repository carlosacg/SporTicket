from django import forms

from .models import Bill
from apps.location.models import Location

from ..tickets.models import Ticket

class BillForm(forms.ModelForm):
	class Meta:
		CHOICES= (
        ('Efectivo', 'Efectivo'),
        ('Tarjeta de credito', 'Tarjeta de credito'),
        ('Tarjeta de debito', 'Tarjeta de debito'),
        )

		model = Bill
		fields = ['id_profile']
		labels = {
			'id_profile':'Id Usuario',
		}
		widgets ={
			'id_profile':forms.TextInput(attrs={'class':'form-control'}),
		}


class AddTicketsForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ['id']
		labels = {
			'id':'ID Boleto',
		}
		widgets = {
			'id':forms.TextInput(attrs={'class':'form-control'}),
		}


class BuyTicketsLocationForm(forms.Form):
	def query(self,event):
		print(event)
		self.fields['location'].queryset= Location.objects.filter(event=event)
        
	CHOICES= (
        ('Tarjeta de credito', 'Tarjeta de credito'),
        ('Tarjeta de debito', 'Tarjeta de debito'),
        )
	location = forms.ModelChoiceField(Location.objects.all(), required=True)   
	quantity = forms.IntegerField(label='Cantidad boletos',required=False)
	payment = forms.ChoiceField(
		required=False,
		choices=CHOICES,
	)