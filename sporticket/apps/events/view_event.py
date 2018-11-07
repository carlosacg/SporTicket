from django import forms
from apps.events.models import Event


class ViewEvent(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            'name',
            'initial_date',
            'initial_time',
            'place',
            'url',
            'state',
            'capacity',
            'local',
            'visitor',
            'event_type',
        ]
        labels ={
            'name':'Nombre',
            'initial_date':'Fecha Inicio',
            'initial_time':'Hora Inicio',
            'place':'Lugar',
            'url':'url',
            'state':'Estado',
            'capacity':'Capacidad',
            'local':'Local',
            'visitor':'Visitante',
            'event_type':'Tipo de Evento',
        }
        widgets ={
            'name': forms.TextInput(attrs={'class':'w3-input w3-border'}),
            'initial_date': forms.DateInput(attrs={'class':'w3-input w3-border', 'type':'date','id':'myDate','value':'aaaa-mm-dd'}),
            'initial_time': forms.TimeInput(attrs={'class':'w3-input w3-border','type':'time', 'id':'myTime' ,'value':'00:00:00'}),
            'place': forms.TextInput(attrs={'class':'w3-input w3-border'}),
            'url': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'-'}),
            'state': forms.TextInput(attrs={'class':'w3-input w3-border'}),
            'capacity': forms.TextInput(attrs={'class':'w3-input w3-border'}),  
            'local': forms.TextInput(attrs={'class':'w3-input w3-border'}),  
            'visitor': forms.TextInput(attrs={'class':'w3-input w3-border'}),  
            'event_type': forms.TextInput(attrs={'class':'w3-input w3-border'}),
        }