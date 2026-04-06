from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import (
    AuditLogViewSet,
    CitaViewSet,
    ConsultaViewSet,
    DoctorViewSet,
    ExpedienteViewSet,
    PacienteViewSet,
    PerfilViewSet,
    RecetaViewSet,
)
from core.views.auth import CurrentUserView
from core.views.dashboard import DashboardView
from core.views.pdf import ConsultaPDFView

router = DefaultRouter()
router.register(r"pacientes", PacienteViewSet)
router.register(r"citas", CitaViewSet)
router.register(r"consultas", ConsultaViewSet)
router.register(r"expedientes", ExpedienteViewSet)
router.register(r"recetas", RecetaViewSet)
router.register(r"doctores", DoctorViewSet)
router.register(r"perfiles", PerfilViewSet)
router.register(r"auditoria", AuditLogViewSet, basename="auditoria")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/auth/", include("core.auth.urls")),
    path("api/auth/me/", CurrentUserView.as_view()),
    path("api/dashboard/", DashboardView.as_view()),
    path("api/consultas/<int:pk>/pdf/", ConsultaPDFView.as_view()),
    path("api/", include(router.urls)),
]
