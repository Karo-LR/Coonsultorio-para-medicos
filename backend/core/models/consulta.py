from django.db import models
from .cita import Cita

class Consulta(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    diagnostico = models.TextField()
    tratamiento = models.TextField()

    def __str__(self):
        return f"Consulta {self.cita}"