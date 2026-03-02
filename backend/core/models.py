from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Expediente(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    alergias = models.TextField(blank=True)
    enfermedades_cronicas = models.TextField(blank=True)


class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=50, default="Pendiente")


class Consulta(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    diagnostico = models.TextField()
    tratamiento = models.TextField()


class Receta(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    medicamento = models.CharField(max_length=100)
    dosis = models.CharField(max_length=100)
    indicaciones = models.TextField()
