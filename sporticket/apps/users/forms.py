from django import forms
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User
from apps.users.models import Profile

class UserForm(UserCreationForm):

	class Meta:
		model = User
		fields = [
				'username',
				'first_name',
				'last_name',
				'email',
				'password1',
				'password2',
		]
		labels = {
				'username': 'Nick',
				'first_name': 'Nombre',
				'last_name': 'Apellido',
				'email': 'Correo electronico',
				'password1': 'Contraseña',
				'password2': 'Confirmación de contraseña',
		}
		widgets = {
				'username':forms.TextInput(attrs={'class':'w3-input w3-border'}),
				'first_name':forms.TextInput(attrs={'class':'w3-input w3-border'}),
				'last_name':forms.TextInput(attrs={'class':'w3-input w3-border'}),
				'email':forms.TextInput(attrs={'class':'w3-input w3-border'}),
				'password1':forms.CharField(widget=forms.PasswordInput()),
				'password2':forms.CharField(widget=forms.PasswordInput()),
		}

class ProfileForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = [    
				'identification',
				'userType',
				'phone',
				'numAccount',
		]
		labels = {
				'identification': 'Identificacion',
				'userType': 'Tipo de usuario',
				'phone': 'Telefono o celular',
				'numAccount': 'Numero de cuenta',
		}
		widgets = {
				'identification':forms.TextInput(attrs={'class':'w3-input w3-border','type':'number'}),
				'userType':forms.TextInput(attrs={'class':'w3-input w3-border'}),
				'phone':forms.TextInput(attrs={'class':'w3-input w3-border','type':'number'}),
				'numAccount':forms.TextInput(attrs={'class':'w3-input w3-border','type':'number'}),
		}

