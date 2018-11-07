from django import forms
 
class ImageForm(forms.Form):
 filename = forms.CharField(max_length=100)
 docfile = forms.ImageField(
        label='Selecciona una imagen'
    )