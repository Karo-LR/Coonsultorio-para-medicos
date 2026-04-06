from rest_framework import filters, viewsets

from core.audit import log_event, snapshot_instance
from core.models import Cita
from core.permissions import IsAdminOrRecepcion, IsStaffRole, get_user_role
from core.serializers import CitaSerializer


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.select_related("paciente", "medico").all().order_by("fecha")
    serializer_class = CitaSerializer
    permission_classes = [IsStaffRole]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["fecha", "estado", "created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminOrRecepcion()]
        return [IsStaffRole()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if get_user_role(self.request.user) == "doctor":
            queryset = queryset.filter(medico=self.request.user)
        paciente_id = self.request.query_params.get("paciente")
        doctor_id = self.request.query_params.get("doctor")
        estado = self.request.query_params.get("estado")
        fecha = self.request.query_params.get("fecha")

        if paciente_id:
            queryset = queryset.filter(paciente_id=paciente_id)
        if doctor_id:
            queryset = queryset.filter(medico_id=doctor_id)
        if estado:
            queryset = queryset.filter(estado=estado)
        if fecha:
            queryset = queryset.filter(fecha__date=fecha)

        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        log_event(
            self.request,
            action="medical.appointment_created",
            instance=instance,
            description="Cita creada.",
            metadata={"after": snapshot_instance(instance)},
        )

    def perform_update(self, serializer):
        before = snapshot_instance(self.get_object())
        instance = serializer.save()
        log_event(
            self.request,
            action="medical.appointment_updated",
            instance=instance,
            description="Cita actualizada.",
            metadata={"before": before, "after": snapshot_instance(instance)},
        )

    def perform_destroy(self, instance):
        snapshot = snapshot_instance(instance)
        log_event(
            self.request,
            action="medical.appointment_deleted",
            instance=instance,
            description="Cita eliminada.",
            metadata={"before": snapshot},
        )
        instance.delete()
