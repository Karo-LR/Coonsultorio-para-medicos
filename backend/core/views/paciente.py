from rest_framework import filters, viewsets

from core.models import Paciente
from core.audit import log_event, snapshot_instance
from core.permissions import IsAdminOrRecepcion, IsStaffRole, get_user_role
from core.serializers import PacienteSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by("-id")
    serializer_class = PacienteSerializer
    permission_classes = [IsStaffRole]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "apellido", "telefono", "direccion"]
    ordering_fields = ["id", "nombre", "apellido", "fecha_nacimiento"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminOrRecepcion()]
        return [IsStaffRole()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if get_user_role(self.request.user) == "doctor":
            queryset = queryset.filter(cita__medico=self.request.user).distinct()
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        log_event(
            self.request,
            action="medical.patient_created",
            instance=instance,
            description="Paciente creado.",
            metadata={"after": snapshot_instance(instance)},
        )

    def perform_update(self, serializer):
        before = snapshot_instance(self.get_object())
        instance = serializer.save()
        log_event(
            self.request,
            action="medical.patient_updated",
            instance=instance,
            description="Paciente actualizado.",
            metadata={"before": before, "after": snapshot_instance(instance)},
        )

    def perform_destroy(self, instance):
        snapshot = snapshot_instance(instance)
        log_event(
            self.request,
            action="medical.patient_deleted",
            instance=instance,
            description="Paciente eliminado.",
            metadata={"before": snapshot},
        )
        instance.delete()
