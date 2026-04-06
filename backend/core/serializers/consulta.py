import bleach
from rest_framework import serializers

from core.models import Consulta


class ConsultaSerializer(serializers.ModelSerializer):
    paciente_id = serializers.IntegerField(source="cita.paciente_id", read_only=True)
    paciente_nombre = serializers.CharField(source="cita.paciente.__str__", read_only=True)
    doctor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Consulta
        fields = "__all__"

    def validate_diagnostico(self, value):
        cleaned = bleach.clean(value).strip()
        if len(cleaned) < 10:
            raise serializers.ValidationError("El diagnostico debe tener mas detalle.")
        return cleaned

    def validate_tratamiento(self, value):
        cleaned = bleach.clean(value).strip()
        if len(cleaned) < 5:
            raise serializers.ValidationError("El tratamiento es obligatorio.")
        return cleaned

    def get_doctor_nombre(self, obj):
        return obj.cita.medico.get_full_name().strip() or obj.cita.medico.username
