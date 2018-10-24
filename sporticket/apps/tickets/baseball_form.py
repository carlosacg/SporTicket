from django import forms
from django.forms import ModelForm
from apps.tickets.models import Ticket



class BaseballForm(forms.ModelForm):
    higthZone= forms.IntegerField(label='Zona Alta',required=False)
    mediumZone= forms.IntegerField(label='Zona Media',required=False)
    lowZone= forms.IntegerField(label='Zona Baja',required=False)
    costHigth=forms.IntegerField(label='Precio Zona Alta',required=False)
    costMediun=forms.IntegerField(label='Precio Zona Alta',required=False)
    costLow=forms.IntegerField(label='Precio Zona Alta',required=False)

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
            'state': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'DISPONIBLE'}),

        }