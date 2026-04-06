from django.utils import timezone
from rest_framework import serializers

from core.models import Cita


class CitaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(source="paciente.__str__", read_only=True)
    doctor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        fields = "__all__"

    def validate_fecha(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("No puedes agendar una cita en el pasado.")
        return value

    def validate(self, attrs):
        paciente = attrs.get("paciente") or getattr(self.instance, "paciente", None)
        medico = attrs.get("medico") or getattr(self.instance, "medico", None)
        fecha = attrs.get("fecha") or getattr(self.instance, "fecha", None)

        if not (paciente and medico and fecha):
            return attrs

        medico_rol = getattr(getattr(medico, "perfil", None), "rol", "")
        if medico_rol != "doctor":
            raise serializers.ValidationError({"medico": "La cita solo puede asignarse a un usuario con rol doctor."})

        conflicto = (
            Cita.objects.filter(medico=medico, fecha=fecha)
            .exclude(pk=getattr(self.instance, "pk", None))
            .exists()
        )
        if conflicto:
            raise serializers.ValidationError(
                {"fecha": "El doctor ya tiene una cita programada en ese horario."}
            )

        return attrs

    def get_doctor_nombre(self, obj):
        return obj.medico.get_full_name().strip() or obj.medico.username
