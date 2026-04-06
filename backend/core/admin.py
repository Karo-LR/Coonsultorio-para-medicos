from django.contrib import admin
from core.models import (
    AuditLog,
    Paciente,
    Cita,
    Consulta,
    Expediente,
    Receta,
    Perfil
)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono')
    search_fields = ('nombre', 'apellido')


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha', 'estado')
    list_filter = ('estado',)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('cita',)


@admin.register(Expediente)
class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ('paciente',)


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('medicamento', 'dosis')


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "actor", "action", "resource_type", "resource_id")
    list_filter = ("action", "resource_type", "created_at")
    search_fields = ("actor__username", "resource_repr", "description")
