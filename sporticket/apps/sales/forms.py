from django import forms

from .models import Bill
from ..tickets.models import Ticket

class BillForm(forms.ModelForm):
	class Meta:
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

class BuyTicketsFormBaseball(forms.Form):
	CHOICES= (
        ('Zona alta', 'Zona alta'),
        ('Zona media', 'Zona media'),
        ('Zona baja', 'Zona baja'),
    	)

	ubication= forms.ChoiceField(choices=CHOICES)
	quantity = forms.IntegerField(label='Cantidad boletos',required=False)

class BuyTicketsForm(forms.Form):
	CHOICES= (
        ('Tribuna norte', 'Tribuna norte'),
        ('Tribuna sur', 'Tribuna sur'),
        ('Tribuna oriente', 'Tribuna oriente'),
		('Tribuna occidente', 'Tribuna occidente'),
    	)

	ubication= forms.ChoiceField(choices=CHOICES)
	quantity = forms.IntegerField(label='Cantidad boletos',required=False)
