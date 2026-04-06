from core.models import Doctor
from core.permissions import IsStaffRole
from core.serializers import DoctorSerializer
from rest_framework import viewsets


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.filter(perfil__rol="doctor", is_active=True).order_by("first_name", "last_name")
    serializer_class = DoctorSerializer
    permission_classes = [IsStaffRole]
