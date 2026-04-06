from rest_framework import serializers

from core.models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()
    rol = serializers.CharField(source="perfil.rol", read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "nombre",
            "rol",
        ]

    def get_nombre(self, obj):
        return obj.get_full_name().strip() or obj.username
