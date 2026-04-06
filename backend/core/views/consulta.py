from rest_framework import filters, viewsets
from rest_framework.exceptions import PermissionDenied

from core.audit import log_event, snapshot_instance
from core.models import Consulta
from core.permissions import IsAdminOrDoctor, get_user_role
from core.serializers import ConsultaSerializer


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.select_related("cita", "cita__paciente", "cita__medico").all().order_by(
        "-cita__fecha"
    )
    serializer_class = ConsultaSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["cita__fecha"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminOrDoctor()]
        return [IsAdminOrDoctor()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if get_user_role(self.request.user) == "doctor":
            queryset = queryset.filter(cita__medico=self.request.user)
        paciente_id = self.request.query_params.get("paciente")
        cita_id = self.request.query_params.get("cita")

        if paciente_id:
            queryset = queryset.filter(cita__paciente_id=paciente_id)
        if cita_id:
            queryset = queryset.filter(cita_id=cita_id)

        return queryset

    def perform_create(self, serializer):
        cita = serializer.validated_data["cita"]
        if get_user_role(self.request.user) == "doctor" and cita.medico_id != self.request.user.id:
            raise PermissionDenied("Solo puedes registrar consultas de tus propias citas.")

        instance = serializer.save()
        log_event(
            self.request,
            action="medical.consultation_created",
            instance=instance,
            description="Consulta creada.",
            metadata={"after": snapshot_instance(instance)},
        )

    def perform_update(self, serializer):
        cita = serializer.validated_data.get("cita", self.get_object().cita)
        if get_user_role(self.request.user) == "doctor" and cita.medico_id != self.request.user.id:
            raise PermissionDenied("Solo puedes modificar consultas de tus propias citas.")

        before = snapshot_instance(self.get_object())
        instance = serializer.save()
        log_event(
            self.request,
            action="medical.consultation_updated",
            instance=instance,
            description="Consulta actualizada.",
            metadata={"before": before, "after": snapshot_instance(instance)},
        )

    def perform_destroy(self, instance):
        snapshot = snapshot_instance(instance)
        log_event(
            self.request,
            action="medical.consultation_deleted",
            instance=instance,
            description="Consulta eliminada.",
            metadata={"before": snapshot},
        )
        instance.delete()
