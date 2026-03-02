from rest_framework import serializers
from .models import Paciente, Cita, Consulta, Receta, Expediente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'


class ExpedienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expediente
        fields = '__all__'


class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'


class RecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receta
        fields = '__all__'