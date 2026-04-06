from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from core.audit import log_event, snapshot_instance
from core.models import Expediente
from core.permissions import IsAdminOrDoctor, get_user_role
from core.serializers import ExpedienteSerializer


class ExpedienteViewSet(viewsets.ModelViewSet):
    queryset = Expediente.objects.select_related("paciente").all().order_by("paciente__apellido")
    serializer_class = ExpedienteSerializer
    permission_classes = [IsAdminOrDoctor]

    def get_queryset(self):
        queryset = super().get_queryset()
        if get_user_role(self.request.user) == "doctor":
            queryset = queryset.filter(paciente__cita__medico=self.request.user).distinct()
        paciente_id = self.request.query_params.get("paciente")

        if paciente_id:
            queryset = queryset.filter(paciente_id=paciente_id)

        return queryset

    def perform_create(self, serializer):
        paciente = serializer.validated_data["paciente"]
        if get_user_role(self.request.user) == "doctor":
            doctor_has_access = paciente.cita_set.filter(medico=self.request.user).exists()
            if not doctor_has_access:
                raise PermissionDenied("Solo puedes crear expedientes de tus propios pacientes.")

        instance = serializer.save()
        log_event(
            self.request,
            action="medical.record_created",
            instance=instance,
            description="Expediente creado.",
            metadata={"after": snapshot_instance(instance)},
        )

    def perform_update(self, serializer):
        paciente = serializer.validated_data.get("paciente", self.get_object().paciente)
        if get_user_role(self.request.user) == "doctor":
            doctor_has_access = paciente.cita_set.filter(medico=self.request.user).exists()
            if not doctor_has_access:
                raise PermissionDenied("Solo puedes modificar expedientes de tus propios pacientes.")

        before = snapshot_instance(self.get_object())
        instance = serializer.save()
        log_event(
            self.request,
            action="medical.record_updated",
            instance=instance,
            description="Expediente actualizado.",
            metadata={"before": before, "after": snapshot_instance(instance)},
        )

    def perform_destroy(self, instance):
        snapshot = snapshot_instance(instance)
        log_event(
            self.request,
            action="medical.record_deleted",
            instance=instance,
            description="Expediente eliminado.",
            metadata={"before": snapshot},
        )
        instance.delete()
