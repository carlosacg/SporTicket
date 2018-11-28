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
		
		