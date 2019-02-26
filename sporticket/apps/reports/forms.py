from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
from datetimewidget.widgets import DateWidget
import datetime
from apps.events.models import Event
from apps.users.models import User
from django.forms.fields import DateField

class ByEventsForms(forms.Form):
    events = forms.ModelChoiceField(queryset=Event.objects.all().values('name'), widget=Select2Widget, required=True)
    users = forms.ModelChoiceField(queryset=User.objects.all().values('first_name'), widget=Select2Widget, required=True)
    numEventAvaible = forms.CharField(label='Ingrese un evento')
    numEventsSale = forms.CharField(label='Ingrese un evento')
    userTickets = forms.CharField(label='Ingrese un evento')
    shoptTickets = forms.CharField(label='Ingrese un evento')
    date1 = forms.DateTimeField()
    date2 = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        super(ByEventsForms, self).__init__(*args, **kwargs)
        
        self.fields['events'].widget.attrs.update({'placeholder':'Eventos', 'required':'required'})
        self.fields['events'].label = 'Seleccione su evento'
        self.fields['users'].widget.attrs.update({'placeholder':'Usuarios', 'required':'required'})
        self.fields['users'].label = 'Seleccione su usuario'
        self.fields['numEventAvaible'].widget.attrs.update({'placeholder':'Disponibles', 'required':'required'})
        self.fields['numEventAvaible'].label = 'Numero de boletos disponibles'
        self.fields['numEventsSale'].widget.attrs.update({'placeholder':'Vendidos', 'required':'required'})
        self.fields['numEventsSale'].label = 'Numero de boletos vendidos'
        self.fields['userTickets'].widget.attrs.update({'placeholder':'Disponibles', 'required':'required'})
        self.fields['userTickets'].label = 'Numero de boletos vendidos'
        self.fields['shoptTickets'].widget.attrs.update({'placeholder':'Vendidos', 'required':'required'})
        self.fields['shoptTickets'].label = 'Numero de boletos comprados'