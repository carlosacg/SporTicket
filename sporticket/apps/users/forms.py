from django import forms
from apps.users.models import Users

class UserForm(forms.ModelForm):

	class Meta:
		model = Users
        
		fields = [
			'identification',
			'name',
			'lastName',
			'email',
			'userType',
			'phone',
			'numAccount',
			'state',
		]
		labels = {
			'identification': 'Identificación',
			'name': 'Nombre',
			'lastName':'Apellido',
			'email': 'Correo',
			'userType': 'Tipo',
			'phone': 'Teléfono',
			'numAccount': 'Número de Cuenta',
			'state': 'Estado',
		}
		widgets = {
			'identification': forms.TextInput(attrs={'class':'w3-input w3-border'}),
			'name': forms.TextInput(attrs={'class':'w3-input w3-border'}),
			'lastName': forms.TextInput(attrs={'class':'w3-input w3-border'}),
			'email': forms.EmailInput(attrs={'class':'w3-input w3-border'}),
			'userType': forms.TextInput(attrs={'class':'w3-input w3-border'}),
			'phone': forms.TextInput(attrs={'class':'w3-input w3-border'}),
			'numAccount': forms.TextInput(attrs={'class':'w3-input w3-border'}),
			'state': forms.TextInput(attrs={'class':'w3-input w3-border','type':'hidden','value':'ACTIVO'}),
		}