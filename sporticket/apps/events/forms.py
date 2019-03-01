from django import forms
from apps.events.models import Event
from apps.events.models import EventImage

class ImageForm(forms.Form):
 filename = forms.CharField(max_length=100)
 docfile = forms.ImageField(
        label='Selecciona una imagen'
    )

class UploadForm(forms.Form):
 filename = forms.CharField(max_length=100)
 docfile = forms.FileField(
        label='Selecciona un archivo'
    )

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        
        CHOICES= (
        ('Futbol', 'Futbol'),
        ('Beisbol', 'Beisbol'),
        ('Tenis', 'Tenis'),
        )
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
            'initial_date':'Fecha inicio',
            'initial_time':'Hora inicio',
            'place':'Lugar',
            'url':'url',
            'state':'Estado',
            'capacity':'Capacidad',
            'local':'Equipo local',
            'visitor':'Equipo visitante',
            'event_type':'Tipo de evento',
        }
        widgets ={
            'name': forms.TextInput(attrs={'class':'w3-input w3-border'}),
            'initial_date': forms.DateInput(attrs={'class':'w3-input w3-border', 'type':'date','id':'myDate','value':'aaaa-mm-dd'}),
            'initial_time': forms.TimeInput(attrs={'class':'w3-input w3-border','type':'time', 'id':'myTime' ,'value':'00:00:00'}),
            'place': forms.TextInput(attrs={'class':'w3-input w3-border'}),
            'url': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'-'}),
            'state': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'Activo'}),
            'capacity': forms.NumberInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'0'}),  
            'local': forms.TextInput(attrs={'class':'w3-input w3-border'}),  
            'visitor': forms.TextInput(attrs={'class':'w3-input w3-border'}),  
            'event_type': forms.Select(choices=CHOICES,attrs={'class':'w3-input w3-border'}),
        }
 
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ['event', 'image']