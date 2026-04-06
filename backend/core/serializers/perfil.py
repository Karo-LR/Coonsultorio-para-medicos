from rest_framework import serializers

from core.models import Perfil


class PerfilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    nombre = serializers.SerializerMethodField()
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Perfil
        fields = ["id", "user", "username", "nombre", "email", "rol"]
        read_only_fields = ["user"]

    def get_nombre(self, obj):
        return obj.user.get_full_name().strip() or obj.user.username

    def validate_rol(self, value):
        instance = getattr(self, "instance", None)
        current_role = getattr(instance, "rol", None)

        if current_role == "admin" and value != "admin":
            raise serializers.ValidationError("El administrador unico del sistema no puede cambiar de rol desde este endpoint.")

        if value == "admin" and getattr(instance, "rol", None) != "admin":
            raise serializers.ValidationError("No se pueden crear ni promover mas administradores.")
        return value
