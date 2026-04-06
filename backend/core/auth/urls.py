from django.urls import path

from core.auth.views import (
    LoginView,
    PasswordResetConfirmView,
    PasswordResetView,
    RegisterView,
    VerifyEmailView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("verify-email/", VerifyEmailView.as_view(), name="auth-verify-email"),
    path("password-reset/", PasswordResetView.as_view(), name="auth-password-reset"),
    path(
        "password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="auth-password-reset-confirm",
    ),
]
