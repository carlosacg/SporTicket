from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
from apps.events.models import Event
from apps.users.models import User
from django.forms.fields import DateField

class ByEventsForms(forms.Form):
    
    events = forms.ModelChoiceField(Event.objects.all() , widget=forms.Select(attrs={'class':'w3-input w3-border'}), required=True)
    ticketsAvailable = forms.DateField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'0'}))
    ticketsSold = forms.DateField(widget=forms.NumberInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'0'}))
    # users = forms.ModelChoiceField(queryset=User.objects.all().values('first_name'), widget=Select2Widget, required=True)


    def __init__(self, *args, **kwargs):
        super(ByEventsForms, self).__init__(*args, **kwargs)
        
        self.fields['events'].widget.attrs.update({'placeholder':'Eventos', 'required':'required'})
        self.fields['events'].label = 'Seleccione su evento'
        self.fields['ticketsAvailable'].label = 'Número de boletos disponibles:'
        self.fields['ticketsSold'].label = 'Número de boletos vendidos:'
        # self.fields['users'].widget.attrs.update({'placeholder':'Usuarios', 'required':'required'})
        # self.fields['users'].label = 'Seleccione su usuario'
        
class ByDateRangeForms(forms.Form):

    dateInitial = forms.DateField(widget=forms.DateInput(attrs={'class':'w3-input w3-border', 'type':'date','id':'myDate','value':'aaaa-mm-dd'}))
    dateFinal = forms.DateField(widget=forms.DateInput(attrs={'class':'w3-input w3-border', 'type':'date','id':'myDate','value':'aaaa-mm-dd'}))
    
    def __init__(self, *args, **kwargs):
        super(ByDateRangeForms, self).__init__(*args, **kwargs)
        
        self.fields['dateInitial'].widget.attrs.update({'placeholder':'Eventos', 'required':'required'})
        self.fields['dateInitial'].label = 'Seleccione su fecha inicial'
        self.fields['dateFinal'].widget.attrs.update({'placeholder':'Usuarios', 'required':'required'})
        self.fields['dateFinal'].label = 'Seleccione su fecha final'