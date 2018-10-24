from django import forms
from django.forms import ModelForm
from apps.tickets.models import Ticket



class TicketForm(forms.ModelForm):
    quantity= forms.IntegerField(label='Cantida Boletos',required=False)


    class Meta:
        model = Ticket
        CHOICES= (
        ('ZONA ALTA', 'ZONA ALTA'),
        ('ZONA MEDIA', 'ZONA MEDIA'),
        ('ZONA BAJA', 'ZONA BAJA'),
        ('TRIBUNA SUR', 'TRIBUNA SUR'),
        ('TRIBUNA NORTE', 'TRIBUNA NORTE'),
        ('TRIBUNA ORIENTE', 'TRIBUNA ORIENTE'),
        ('TRIBUNA OCCIDENTE', 'TRIBUNA OCCIDENTE'),
        )
        fields = [
            'ubication',
            'cost',
            'event',
            'state',
        ]
        labels ={
            'ubication':'Ubicacion',
            'cost':'Precio',
            'event':'Evento',
            'state':'Estado',
        }
        widgets ={
            'ubication': forms.Select(choices=CHOICES,attrs={'class':'w3-input w3-border'}),
            'cost': forms.NumberInput(attrs={'class':'w3-input w3-border'}),
            'event': forms.Select(attrs={'class':'w3-input w3-border','type':'time', 'id':'myTime' ,'value':'00:00:00'}),        
            'state': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'EN VENTA'}),

        }

