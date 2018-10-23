from django import forms
from django.forms import ModelForm
from apps.tickets.models import Ticket



class BaseballForm(forms.ModelForm):
    quantity= forms.IntegerField(label='Cantida Boletos',required=False)


    class Meta:
        model = Ticket
        CHOICES= (
        ('ZONA ALTA', 'ZONA ALTA'),
        ('ZONA MEDIA', 'ZONA MEDIA'),
        ('ZONA BAJA', 'ZONA BAJA'),
        )
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
            'ubication': forms.Select(choices=CHOICES,attrs={'class':'w3-input w3-border'}),
            'cost': forms.NumberInput(attrs={'class':'w3-input w3-border'}),
            'state': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'DISPONIBLE'}),

        }