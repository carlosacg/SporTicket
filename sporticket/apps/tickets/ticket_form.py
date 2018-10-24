from django import forms
from django.forms import ModelForm
from apps.tickets.models import Ticket



class TicketForm(forms.ModelForm):
    northZone= forms.IntegerField(label='Tribuna Norte',required=False)
    southZone= forms.IntegerField(label='Tribuna Sur',required=False)
    eastZone= forms.IntegerField(label='Tribuna Oriente',required=False)
    westZone= forms.IntegerField(label='Tribuna Occidente',required=False)
    costNorth=forms.IntegerField(label='Precio Tribuna Norte',required=False)
    costSouth=forms.IntegerField(label='Precio Tribuna Sur',required=False)
    costEast=forms.IntegerField(label='Precio Tribuna Oriente',required=False)
    costWest=forms.IntegerField(label='Precio Tribuna Occidente',required=False)

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

