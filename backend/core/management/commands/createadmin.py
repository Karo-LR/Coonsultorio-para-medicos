from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import Perfil


class Command(BaseCommand):
    help = "Crea el admin inicial solo cuando la base de datos esta vacia."

    def handle(self, *args, **kwargs):
        User = get_user_model()

        existing_admin = Perfil.objects.select_related("user").filter(rol="admin").first()
        if existing_admin:
            self.stdout.write(
                self.style.WARNING(
                    f"Ya existe un administrador: {existing_admin.user.username}. No se puede crear otro."
                )
            )
            return

        if User.objects.exists():
            self.stdout.write(
                self.style.ERROR(
                    "La base de datos no esta vacia. Borra los usuarios primero si quieres crear un admin inicial nuevo."
                )
            )
            return

        username = "admin"
        email = "kath22319@gmail.com"
        password = "Pozoldecacao123*"

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=["is_active", "is_staff", "is_superuser"])

        perfil = user.perfil
        perfil.rol = "admin"
        perfil.save(update_fields=["rol"])

        self.stdout.write(self.style.SUCCESS("Admin inicial creado correctamente."))
        self.stdout.write(f"username: {username}")
        self.stdout.write(f"email: {email}")
        self.stdout.write(f"password: {password}")
