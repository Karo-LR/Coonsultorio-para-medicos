from rest_framework import viewsets
from .models import Paciente, Cita, Consulta, Receta, Expediente
from .serializers import *


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


class ExpedienteViewSet(viewsets.ModelViewSet):
    queryset = Expediente.objects.all()
    serializer_class = ExpedienteSerializer


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer


class RecetaViewSet(viewsets.ModelViewSet):
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer