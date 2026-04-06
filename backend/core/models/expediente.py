from django.db import models
from .paciente import Paciente

class Expediente(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    alergias = models.TextField(blank=True)
    enfermedades_cronicas = models.TextField(blank=True)

    def __str__(self):
        return f"Expediente de {self.paciente}"