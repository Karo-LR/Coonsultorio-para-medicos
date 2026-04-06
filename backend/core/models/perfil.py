from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Perfil(models.Model):
    ROLES = (
        ("admin", "Administrador"),
        ("doctor", "Doctor"),
        ("recepcionista", "Recepcionista"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default="recepcionista")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["rol"],
                condition=Q(rol="admin"),
                name="unique_admin_role",
            )
        ]

    def clean(self):
        super().clean()
        if self.rol == "admin":
            admin_exists = Perfil.objects.filter(rol="admin").exclude(pk=self.pk).exists()
            if admin_exists:
                raise ValidationError({"rol": "Ya existe un administrador registrado."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
