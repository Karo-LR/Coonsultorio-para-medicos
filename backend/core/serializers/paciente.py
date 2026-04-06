from rest_framework import serializers

from core.models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Paciente
        fields = "__all__"

    def validate_telefono(self, value):
        telefono = "".join(char for char in value if char.isdigit())
        if len(telefono) < 8:
            raise serializers.ValidationError("Ingresa un telefono valido.")
        return telefono

    def validate_nombre(self, value):
        value = value.strip().title()
        if len(value) < 2:
            raise serializers.ValidationError("Nombre muy corto.")
        return value

    def validate_apellido(self, value):
        value = value.strip().title()
        if len(value) < 2:
            raise serializers.ValidationError("Apellido muy corto.")
        return value

    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}".strip()
