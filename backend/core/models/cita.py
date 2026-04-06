from django.db import models
from django.contrib.auth.models import User
from .paciente import Paciente

class Cita(models.Model):

    ESTADOS = (
        ("pendiente","Pendiente"),
        ("confirmada","Confirmada"),
        ("completada","Completada"),
    )

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(User, on_delete=models.CASCADE)

    fecha = models.DateTimeField()
    motivo = models.TextField()

    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")

    # 🔥 AUDITORÍA
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)