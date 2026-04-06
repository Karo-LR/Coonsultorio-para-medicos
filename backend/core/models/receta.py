from django.db import models
from .consulta import Consulta

class Receta(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    medicamento = models.CharField(max_length=100)
    dosis = models.CharField(max_length=100)
    indicaciones = models.TextField()

    def __str__(self):
        return self.medicamento