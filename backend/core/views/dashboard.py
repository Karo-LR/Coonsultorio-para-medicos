from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Cita, Consulta, Paciente
from core.permissions import get_user_role


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hoy = timezone.localdate()
        rol = get_user_role(request.user)

        if rol == "admin":
            citas_recientes = Cita.objects.select_related("paciente", "medico").order_by("-fecha")[:8]
            consultas_recientes = Consulta.objects.select_related("cita", "cita__paciente").order_by("-cita__fecha")[:5]
            return Response(
                {
                    "rol": rol,
                    "metricas": {
                        "pacientes_totales": Paciente.objects.count(),
                        "citas_hoy": Cita.objects.filter(fecha__date=hoy).count(),
                        "doctores_activos": User.objects.filter(
                            perfil__rol="doctor",
                            is_active=True,
                        ).count(),
                        "consultas_recientes": Consulta.objects.count(),
                    },
                    "citas_recientes": [
                        {
                            "id": cita.id,
                            "paciente": str(cita.paciente),
                            "doctor": cita.medico.get_full_name().strip() or cita.medico.username,
                            "fecha": cita.fecha,
                            "estado": cita.estado,
                            "motivo": cita.motivo,
                        }
                        for cita in citas_recientes
                    ],
                    "consultas_recientes": [
                        {
                            "id": consulta.id,
                            "paciente": str(consulta.cita.paciente),
                            "fecha": consulta.cita.fecha,
                            "diagnostico": consulta.diagnostico,
                        }
                        for consulta in consultas_recientes
                    ],
                }
            )

        if rol == "doctor":
            citas_queryset = Cita.objects.select_related("paciente", "medico").filter(medico=request.user)
            consultas_queryset = Consulta.objects.select_related("cita", "cita__paciente").filter(cita__medico=request.user)
            return Response(
                {
                    "rol": rol,
                    "metricas": {
                        "mis_pacientes": Paciente.objects.filter(cita__medico=request.user).distinct().count(),
                        "mis_citas_hoy": citas_queryset.filter(fecha__date=hoy).count(),
                        "mis_consultas": consultas_queryset.count(),
                    },
                    "citas_recientes": [
                        {
                            "id": cita.id,
                            "paciente": str(cita.paciente),
                            "fecha": cita.fecha,
                            "estado": cita.estado,
                            "motivo": cita.motivo,
                        }
                        for cita in citas_queryset.order_by("-fecha")[:8]
                    ],
                    "consultas_recientes": [
                        {
                            "id": consulta.id,
                            "paciente": str(consulta.cita.paciente),
                            "fecha": consulta.cita.fecha,
                            "diagnostico": consulta.diagnostico,
                        }
                        for consulta in consultas_queryset.order_by("-cita__fecha")[:5]
                    ],
                }
            )

        citas_queryset = Cita.objects.select_related("paciente", "medico").order_by("-fecha")
        return Response(
            {
                "rol": rol,
                "metricas": {
                    "pacientes_totales": Paciente.objects.count(),
                    "citas_hoy": citas_queryset.filter(fecha__date=hoy).count(),
                    "citas_pendientes": citas_queryset.filter(estado="pendiente").count(),
                },
                "citas_recientes": [
                    {
                        "id": cita.id,
                        "paciente": str(cita.paciente),
                        "doctor": cita.medico.get_full_name().strip() or cita.medico.username,
                        "fecha": cita.fecha,
                        "estado": cita.estado,
                        "motivo": cita.motivo,
                    }
                    for cita in citas_queryset[:8]
                ],
            }
        )
