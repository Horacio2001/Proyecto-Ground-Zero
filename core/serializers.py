from rest_framework import serializers 
from .models import *

class TipoEmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEmpleado
        fields = '__all__'

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoGenero
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    tipo = TipoEmpleadoSerializer(read_only=True)
    genero = GeneroSerializer(read_only=True)
    class Meta:
        model = Empleado
        fields = '__all__'

