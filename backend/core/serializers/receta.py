from rest_framework import serializers

from core.models import Receta


class RecetaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(source="consulta.cita.paciente.__str__", read_only=True)

    class Meta:
        model = Receta
        fields = "__all__"
