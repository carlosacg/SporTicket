from django import forms
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
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

		CHOICES= (
        ('Vendedor', 'Vendedor'),
        ('Gerente', 'Gerente'),
        ('Externo', 'Externo'),
        )

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
				'userType':forms.Select(choices=CHOICES,attrs={'class':'w3-input w3-border'}),
				'phone':forms.TextInput(attrs={'class':'w3-input w3-border','type':'number'}),
				'numAccount':forms.TextInput(attrs={'class':'w3-input w3-border','type':'number'}),
		}

class UserUpdateForm(forms.Form):

		CHOICES= (
		('Vendedor', 'Vendedor'),
		('Gerente', 'Gerente'),
		('Externo', 'Externo'),
		)

		userType = forms.ChoiceField(
		required=False,
		choices=CHOICES,
	)
		username = forms.CharField(widget=forms.TextInput(attrs={'class':'w3-input w3-border'}))
		identification = forms.CharField(widget=forms.TextInput(attrs={'class':'w3-input w3-border','type':'number'}))
		first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'w3-input w3-border'}))
		last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'w3-input w3-border'}))
		password = forms.CharField(widget=forms.PasswordInput())
		passwordConfirmation = forms.CharField(widget=forms.PasswordInput())
		email = forms.CharField(widget=forms.TextInput(attrs={'class':'w3-input w3-border'}))
		phone = forms.CharField(widget=forms.TextInput(attrs={'class':'w3-input w3-border','type':'number'}))
		numAccount = forms.CharField(widget=forms.TextInput(attrs={'class':'w3-input w3-border','type':'number'}))
