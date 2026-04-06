from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.text import slugify
from rest_framework import serializers

from core.auth.utils import normalize_email, sanitize_text
from core.models import Perfil


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password_confirm = serializers.CharField(write_only=True, trim_whitespace=False)
    rol = serializers.ChoiceField(choices=["admin", "doctor", "recepcionista"])

    def validate_first_name(self, value):
        value = sanitize_text(value)
        if len(value) < 2:
            raise serializers.ValidationError("El nombre es demasiado corto.")
        return value

    def validate_last_name(self, value):
        return sanitize_text(value)

    def validate_email(self, value):
        email = normalize_email(value)
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Este correo ya esta registrado.")
        return email

    def validate(self, attrs):
        request = self.context.get("request")
        users_exist = User.objects.exists()
        requested_role = attrs["rol"]

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Las contrasenas no coinciden."})

        if not users_exist:
            if requested_role != "admin":
                raise serializers.ValidationError({"rol": "El primer usuario del sistema debe ser administrador."})
        else:
            if requested_role == "admin":
                raise serializers.ValidationError({"rol": "No se pueden crear mas administradores."})

            request_user = getattr(request, "user", None)
            request_role = getattr(getattr(request_user, "perfil", None), "rol", None)
            if not request_user or not request_user.is_authenticated or request_role != "admin":
                raise serializers.ValidationError({"detail": "Solo un administrador autenticado puede crear usuarios."})

        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        is_initial_setup = not User.objects.exists()
        email = validated_data["email"]
        username = self._build_unique_username(email)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data.get("last_name", ""),
            is_active=True,
        )

        perfil = user.perfil
        perfil.rol = validated_data["rol"]
        perfil.save(update_fields=["rol"])
        if is_initial_setup:
            user.is_staff = True
            user.is_superuser = True
            user.save(update_fields=["is_staff", "is_superuser"])
        return user

    def _build_unique_username(self, email):
        base_username = slugify(email.split("@")[0]).replace("-", "") or "usuario"
        username = base_username[:150]
        counter = 1

        while User.objects.filter(username=username).exists():
            suffix = str(counter)
            username = f"{base_username[:150 - len(suffix)]}{suffix}"
            counter += 1

        return username
