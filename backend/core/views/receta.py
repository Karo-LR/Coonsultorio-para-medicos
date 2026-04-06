from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from core.audit import log_event, snapshot_instance
from core.models import Receta
from core.permissions import IsAdminOrDoctor, get_user_role
from core.serializers import RecetaSerializer


class RecetaViewSet(viewsets.ModelViewSet):
    queryset = Receta.objects.select_related("consulta", "consulta__cita", "consulta__cita__paciente").all()
    serializer_class = RecetaSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminOrDoctor()]
        return [IsAdminOrDoctor()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if get_user_role(self.request.user) == "doctor":
            queryset = queryset.filter(consulta__cita__medico=self.request.user)
        consulta_id = self.request.query_params.get("consulta")
        paciente_id = self.request.query_params.get("paciente")

        if consulta_id:
            queryset = queryset.filter(consulta_id=consulta_id)
        if paciente_id:
            queryset = queryset.filter(consulta__cita__paciente_id=paciente_id)

        return queryset

    def perform_create(self, serializer):
        consulta = serializer.validated_data["consulta"]
        if get_user_role(self.request.user) == "doctor" and consulta.cita.medico_id != self.request.user.id:
            raise PermissionDenied("Solo puedes crear recetas de tus propias consultas.")

        instance = serializer.save()
        log_event(
            self.request,
            action="medical.prescription_created",
            instance=instance,
            description="Receta creada.",
            metadata={"after": snapshot_instance(instance)},
        )

    def perform_update(self, serializer):
        consulta = serializer.validated_data.get("consulta", self.get_object().consulta)
        if get_user_role(self.request.user) == "doctor" and consulta.cita.medico_id != self.request.user.id:
            raise PermissionDenied("Solo puedes modificar recetas de tus propias consultas.")

        before = snapshot_instance(self.get_object())
        instance = serializer.save()
        log_event(
            self.request,
            action="medical.prescription_updated",
            instance=instance,
            description="Receta actualizada.",
            metadata={"before": before, "after": snapshot_instance(instance)},
        )

    def perform_destroy(self, instance):
        snapshot = snapshot_instance(instance)
        log_event(
            self.request,
            action="medical.prescription_deleted",
            instance=instance,
            description="Receta eliminada.",
            metadata={"before": snapshot},
        )
        instance.delete()
