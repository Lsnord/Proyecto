from dataclasses import field, fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from core.choices import GENDER_CHOICES
from django.core.exceptions import ValidationError

## crispy-forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions
from django import forms
from core.models import gastos, citas, examenes, tratamientos, terapias, cirugias

##################### Usuario Forms ###########################

## Creacion de Cuenta

class UserRegisterForm(UserCreationForm):
    genero = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    username = forms.CharField(label="Nombre",widget=forms.TextInput(attrs={'placeholder': 'Tu Nombre'}))
    last_name = forms.CharField(label="Apellido",widget=forms.TextInput(attrs={'placeholder': 'Tu Apellido'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Edad'}))
    password1 = forms.CharField(label="Contraseña",widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label="Confirmar contraseña",widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))

    class Meta:
        model = User
        fields = [
            'username',
            'last_name',
            'genero',
            'age',
            'email',
            'password1',
            'password2',
        ]

        help_texts = {k: "" for k in fields}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, usa otro.')
        return email
        
## Inicio de sesion

class LoginForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


##Contacto

class formcontact(forms.Form):

    asunto=forms.CharField(min_length=8, max_length=24)
    email=forms.EmailField()
    mensaje=forms.CharField(min_length=32, max_length=512)
    
##Soporte

class formsoporte(forms.Form):

    asunto=forms.CharField(min_length=8, max_length=24)
    email=forms.EmailField()
    mensaje=forms.CharField(min_length=32, max_length=512)
    
##Informes de errores

class forminformes(forms.Form):

    asunto=forms.CharField(min_length=8, max_length=24)
    email=forms.EmailField()
    mensaje=forms.CharField(min_length=32, max_length=512)

#Historiales

#Gastos
class GastoForm(forms.ModelForm):
    class Meta:
        model = gastos
        fields = ['nombre', 'tipos', 'fecha', 'costo', 'mascota']

#Citas
class CitasForm(forms.ModelForm):
    class Meta:
        model = citas
        fields = ['nombre', 'tipos', 'fecha', 'costo', 'mascota']
        
#Examenes
class ExamenesForm(forms.ModelForm):
    class Meta:
        model = examenes
        fields = ['nombre', 'tipos', 'fecha', 'costo', 'mascota']
        
#Tratamientos 
class TratamientosForm(forms.ModelForm):
    class Meta:
        model = tratamientos
        fields = ['nombre', 'fecha', 'costo', 'mascota']
        
#Terapias
class TerapiasForm(forms.ModelForm):
    class Meta:
        model = terapias
        fields = ['nombre', 'fecha', 'costo', 'mascota']
        
#Cirugias
class CirugiasForm(forms.ModelForm):
    class Meta:
        model = cirugias
        fields = ['nombre', 'tipos', 'fecha', 'costo', 'mascota']                       
