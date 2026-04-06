from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .perfil import Perfil

def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

post_save.connect(crear_perfil, sender=User)