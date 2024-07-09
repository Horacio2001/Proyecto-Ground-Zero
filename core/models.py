from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.views import PasswordContextMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.edit import FormView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
# Create your models here.

#pip install pillow 
#pip install django

class TipoGenero(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion

class TipoEmpleado(models.Model):
    descripcion = models.CharField(max_length=20)
    
    def __str__(self):
        return self.descripcion

class Empleado(models.Model):
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.IntegerField()
    direccion = models.CharField(max_length=60)
    telefono = models.CharField(max_length=14)
    genero = models.ForeignKey(TipoGenero, on_delete=models.PROTECT)
    tipo = models.ForeignKey(TipoEmpleado,on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.rut)

class TipoObra(models.Model):
    descripcion = models.CharField(max_length=30)
    
    def __str__(self):
        return self.descripcion

    
class Obra(models.Model):
    id_obra = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    historia = models.TextField()
    tecnica_usada = models.CharField(max_length=350)
    precio = models.IntegerField()
    foto = models.ImageField(upload_to="obras", null=True)
    tipo = models.ForeignKey(TipoObra,on_delete=models.PROTECT)
    artista = models.ForeignKey(Empleado,on_delete=models.PROTECT, default=1)
    def __str__(self):
        return str(self.id_obra)
    
    # Validar que el precio no sea negativo 
    def clean(self):
        if self.precio < 0:
            raise ValidationError('El precio no puede ser negativo.')

    # Validar que el nombre no pueda estar vacio
        if not self.nombre.strip(): 
            raise ValidationError('El nombre no puede estar vacío o contener solo espacios en blanco.')

    # Validar que que no se repitan cosas iguales
    
        if self.descripcion == self.historia:
            raise ValidationError('La descripción y la historia no pueden ser iguales.')


opciones_consultas = [
    [0,"consulta"],
    [1,"reclamo"],
    [2,"sugerencia"],
    [3,"felicitaciones"]
]

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre

    
class Pago(models.Model):
    identificador_venta = models.CharField(max_length=100)
    nombre_usuario = models.CharField(max_length=150)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_plan = models.CharField(max_length=50)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre_usuario} - {self.nombre_plan}'

    class Meta:
        verbose_name_plural = 'Pagos'
    

