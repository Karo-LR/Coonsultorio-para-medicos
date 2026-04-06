from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.auth.utils import (
    decode_password_reset_token,
    normalize_email,
    send_password_reset_email,
)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return normalize_email(value)

    def save(self, **kwargs):
        email = self.validated_data["email"]
        user = User.objects.filter(email__iexact=email, is_active=True).first()

        if user:
            send_password_reset_email(user)

        return {"detail": "Si el correo existe, enviaremos instrucciones para restablecer la contrasena."}


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password_confirm = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Las contrasenas no coinciden."})

        user = decode_password_reset_token(attrs["token"])
        validate_password(attrs["password"], user=user)
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password"])
        user.save(update_fields=["password"])
        return user
