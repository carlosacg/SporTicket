from django import forms
from apps.login.models import Login

class LoginForm(forms.ModelForm):

	class Meta:
		model = Login
        
		fields = [
			'email',
			'password',
		]
		labels = {
			'email': 'Correo',
			'password': 'Contraseña',
		}
		widgets = {
			'email': forms.EmailInput(attrs={'class':'w3-input w3-border'}),
			'password': forms.PasswordInput(attrs={'class':'w3-input w3-border'}),
		}