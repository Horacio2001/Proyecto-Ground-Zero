from django.contrib import admin
from .models import *
# Register your models here.

class ProductoObra(admin.ModelAdmin):
    list_display=["id_obra","nombre", "precio","tipo","artista"]
    list_editable=["precio"]
    search_fields=["nombre"]
    list_filter=["tipo"]

class DetalleEmpleado(admin.ModelAdmin):
    list_display=["rut","nombre","apellido","tipo"]
    
class DetalleContacto(admin.ModelAdmin):
    list_display=["nombre","correo","tipo_consulta"]


admin.site.register(Obra,ProductoObra)
admin.site.register(TipoObra)
admin.site.register(Empleado,DetalleEmpleado)
admin.site.register(TipoEmpleado)
admin.site.register(TipoGenero)
admin.site.register(Contacto,DetalleContacto)