from django import forms
from .models import Contacto, Obra, TipoObra     
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField


class ContactoForm(forms.ModelForm):
    
    nombre = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'fname', 'name': 'fname', 'placeholder': 'Nombre Completo. '}))
    correo = forms.CharField(widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'id': 'email', 'name': 'email', 'placeholder': 'Ingresa tú gmail.'}))
    opciones_consulta = [
    (0, 'Consulta'),
    (1, 'Reclamo'),
    (2, 'Sugerencia'),
    (3, 'Felicitaciones')
    ]
    tipo_consulta = forms.ChoiceField(choices=opciones_consulta, widget=forms.Select(attrs={'class': 'form-control', 'id': 'subj',}))


    mensaje = forms.CharField(widget=forms.Textarea(attrs={'id': 'mssg', 'name': 'mssg', 'placeholder': 'Ingresa tú mensaje.', 'class': 'form-control', 'rows': '10'}))


    class Meta:
        model = Contacto
        #fields = ["nombre","correo","tipo_consulta","mensaje"] Ya no es necesario ya que con All agarramos todo
        fields = '__all__'


class ObraForm(forms.ModelForm):

    nombre =forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'fname', 'name': 'fname', 'placeholder': 'Ingresa el nombre de tu obra.'}))
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'id': 'mssg', 'name': 'mssg', 'placeholder': 'Ingresa la descripcion.', 'class': 'form-control', 'rows': '10'}))
    historia = forms.CharField(widget=forms.Textarea(attrs={'id': 'mssg', 'name': 'mssg', 'placeholder': 'Ingresa la historia.', 'class': 'form-control', 'rows': '10'}))
    tecnica_usada = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'fname', 'name': 'fname', 'placeholder': 'Tecnica usada.'}))
    precio = forms.DecimalField(widget=forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'id': 'precio', 'name': 'precio', 'placeholder': 'Ingresa el precio.'}))
    foto = forms.ImageField(widget=forms.FileInput(attrs={'type': 'file', 'class': 'form-control-file', 'id': 'imagen', 'name': 'imagen', 'accept': 'image/*'}))
    tipo = forms.ModelChoiceField(queryset=TipoObra.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Obra
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()  
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']   



class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    captcha = CaptchaField()  # Si deseas agregar un campo de captcha

    class Meta:
        model = User
        fields = ['username', 'password']



        
        
