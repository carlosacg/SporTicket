from django import forms
from apps.event_type.models import EventType

class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType

        fields = [
            'name',
        ]
        labels ={
            'name':'Tipo de evento',
        }
        widgets ={
            'name': forms.TextInput(attrs={'class':'w3-input w3-border'}),
        }