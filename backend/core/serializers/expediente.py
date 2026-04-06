from rest_framework import serializers

from core.models import Expediente


class ExpedienteSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(source="paciente.__str__", read_only=True)

    class Meta:
        model = Expediente
        fields = "__all__"
