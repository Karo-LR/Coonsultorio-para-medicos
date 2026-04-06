from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from core.audit import log_event
from core.auth.utils import normalize_email, sanitize_text


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    def validate(self, attrs):
        identifier = sanitize_text(attrs["email"])
        password = attrs["password"]

        candidates = []
        if "@" in identifier:
            candidates.extend(
                User.objects.filter(email__iexact=normalize_email(identifier))
                .order_by("-is_superuser", "-is_staff", "id")
            )
        candidates.extend(
            User.objects.filter(username__iexact=identifier).order_by("-is_superuser", "-is_staff", "id")
        )

        seen = set()
        authenticated_user = None
        for candidate in candidates:
            if candidate.id in seen:
                continue
            seen.add(candidate.id)
            authenticated_user = authenticate(
                request=self.context.get("request"),
                username=candidate.username,
                password=password,
            )
            if authenticated_user:
                break

        if not authenticated_user:
            log_event(
                self.context.get("request"),
                action="auth.login_failed",
                description="Intento de inicio de sesion fallido.",
                metadata={"identifier": identifier},
            )
            raise serializers.ValidationError({"detail": "Credenciales incorrectas."})

        if not authenticated_user.is_active:
            raise serializers.ValidationError(
                {"detail": "Tu cuenta aun no esta activa. Verifica tu correo."}
            )

        refresh = RefreshToken.for_user(authenticated_user)
        perfil = getattr(authenticated_user, "perfil", None)
        refresh["rol"] = getattr(perfil, "rol", "")

        attrs["access"] = str(refresh.access_token)
        attrs["refresh"] = str(refresh)
        attrs["user"] = {
            "id": authenticated_user.id,
            "username": authenticated_user.username,
            "email": authenticated_user.email,
            "rol": getattr(perfil, "rol", ""),
        }
        log_event(
            self.context.get("request"),
            action="auth.login_succeeded",
            instance=authenticated_user,
            description="Inicio de sesion exitoso.",
            metadata={"rol": getattr(perfil, "rol", "")},
        )
        return attrs
