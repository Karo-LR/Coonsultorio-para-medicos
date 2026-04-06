import json
from urllib import parse, request

import bleach
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import signing
from django.core.mail import send_mail
from rest_framework import serializers

EMAIL_VERIFICATION_SALT = "core.auth.verify_email"
PASSWORD_RESET_SALT = "core.auth.password_reset"
password_reset_token_generator = PasswordResetTokenGenerator()


def sanitize_text(value):
    return bleach.clean(value or "", strip=True).strip()


def normalize_email(value):
    return sanitize_text(value).lower()


def send_email(subject, message, recipient_list, html_message=None):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )


def generate_email_verification_token(user):
    return signing.dumps(
        {"user_id": user.id, "email": user.email},
        salt=EMAIL_VERIFICATION_SALT,
    )


def decode_email_verification_token(token):
    max_age = settings.EMAIL_VERIFICATION_TOKEN_MAX_AGE

    try:
        payload = signing.loads(token, salt=EMAIL_VERIFICATION_SALT, max_age=max_age)
    except signing.SignatureExpired as exc:
        raise serializers.ValidationError({"detail": "El token de verificacion ya expiro."}) from exc
    except signing.BadSignature as exc:
        raise serializers.ValidationError({"detail": "El token de verificacion es invalido o expiro."}) from exc

    user = User.objects.filter(id=payload["user_id"], email__iexact=payload["email"]).first()
    if not user:
        raise serializers.ValidationError({"detail": "No se encontro el usuario asociado al token."})
    return user


def build_password_reset_token(user):
    token = password_reset_token_generator.make_token(user)
    return signing.dumps(
        {"user_id": user.id, "token": token},
        salt=PASSWORD_RESET_SALT,
    )


def decode_password_reset_token(token):
    try:
        payload = signing.loads(
            token,
            salt=PASSWORD_RESET_SALT,
            max_age=settings.PASSWORD_RESET_TOKEN_MAX_AGE,
        )
    except signing.SignatureExpired as exc:
        raise serializers.ValidationError({"detail": "El token de recuperacion ya expiro."}) from exc
    except signing.BadSignature as exc:
        raise serializers.ValidationError({"detail": "El token de recuperacion es invalido o expiro."}) from exc

    user = User.objects.filter(id=payload["user_id"]).first()
    if not user or not password_reset_token_generator.check_token(user, payload["token"]):
        raise serializers.ValidationError({"detail": "El token de recuperacion no es valido."})
    return user


def send_verification_email(user, token):
    verify_url = f"{settings.BACKEND_URL.rstrip('/')}/api/auth/verify-email/?token={parse.quote(token)}"
    frontend_url = f"{settings.FRONTEND_URL.rstrip('/')}/login?verified=1" if settings.FRONTEND_URL else verify_url

    message = (
        "Bienvenido al sistema clinico.\n\n"
        f"Activa tu cuenta con este enlace:\n{verify_url}\n\n"
        f"Despues puedes iniciar sesion aqui:\n{frontend_url}\n"
    )
    send_email(
        subject="Activa tu cuenta",
        message=message,
        recipient_list=[user.email],
    )


def send_password_reset_email(user):
    token = build_password_reset_token(user)
    reset_url = (
        f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={parse.quote(token)}"
        if settings.FRONTEND_URL
        else f"{settings.BACKEND_URL.rstrip('/')}/api/auth/password-reset-confirm/"
    )
    message = (
        "Recibimos una solicitud para restablecer tu contrasena.\n\n"
        f"Token: {token}\n"
        f"Enlace sugerido: {reset_url}\n"
    )
    send_email(
        subject="Restablece tu contrasena",
        message=message,
        recipient_list=[user.email],
    )


def validate_recaptcha_or_raise(token, action="submit"):
    if not token:
        raise serializers.ValidationError(
            {"detail": "Debes completar el reCAPTCHA antes de continuar."}
        )

    if not settings.RECAPTCHA_SECRET_KEY:
        raise serializers.ValidationError(
            {"detail": "La validacion reCAPTCHA no esta configurada en el servidor."}
        )

    payload = parse.urlencode(
        {
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": token,
        }
    ).encode()
    req = request.Request(
        "https://www.google.com/recaptcha/api/siteverify",
        data=payload,
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=settings.RECAPTCHA_TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise serializers.ValidationError(
            {"detail": f"No se pudo validar reCAPTCHA para {action}. Intenta de nuevo."}
        ) from exc

    if not data.get("success"):
        error_codes = data.get("error-codes", [])
        if "missing-input-response" in error_codes:
            detail = "Debes completar el reCAPTCHA antes de continuar."
        elif "invalid-input-response" in error_codes:
            detail = "El token de reCAPTCHA es invalido o expiro. Vuelve a intentarlo."
        else:
            detail = "La validacion de reCAPTCHA fallo. Intenta nuevamente."

        raise serializers.ValidationError({"detail": detail})

    return True
