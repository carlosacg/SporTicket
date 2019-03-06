from django import forms
from apps.location.models import Location

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location

        fields = [
            'event',
            'name',
            'cost'

        ]
        labels ={
            'event':'event',
            'name':'Nombre localidad',
            'cost':'Precio localidad'
        }
        widgets ={
            'event': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'-'}),
            'name': forms.TextInput(attrs={'class':'w3-input w3-border'}),
            'cost': forms.NumberInput(attrs={'class':'w3-input w3-border'}),
        }