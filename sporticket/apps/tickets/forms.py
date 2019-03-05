from django import forms
from django.forms import ModelForm
from apps.tickets.models import Ticket




class TicketLocationForm(forms.ModelForm):
    zone= forms.IntegerField(required=False)
    cost=forms.IntegerField(required=False)

    class Meta:
        model = Ticket

        fields = [
            'ubication',
            'cost',
            'state',
        ]
        labels ={
            'ubication':'Ubicacion',
            'cost':'Precio',
            'state':'Estado',
        }
        widgets ={
            'ubication': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'-'}),
            'cost': forms.NumberInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'0'}),
            'state': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'Disponible'}),

        }

