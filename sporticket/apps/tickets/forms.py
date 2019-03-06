from django import forms
from django.forms import ModelForm
from apps.tickets.models import Ticket
from apps.location.models import Location




class TicketLocationForm(forms.ModelForm):

    def query(self,event):
        print(event)
        self.fields['location'].queryset= Location.objects.filter(event=event)
            
    location = forms.ModelChoiceField(Location.objects.all(), required=True)
    zone= forms.IntegerField(required=False)
    class Meta:
        model = Ticket

        fields = [
            'state',
        ]
        labels ={
            'state':'Estado',
        }
        widgets ={
            'state': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'Disponible'}),
        }
