from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'expedientes', ExpedienteViewSet)
router.register(r'citas', CitaViewSet)
router.register(r'consultas', ConsultaViewSet)
router.register(r'recetas', RecetaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/', include(router.urls)),
]