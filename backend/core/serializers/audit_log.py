from rest_framework import serializers

from core.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "actor",
            "actor_username",
            "action",
            "resource_type",
            "resource_id",
            "resource_repr",
            "description",
            "metadata",
            "created_at",
        ]
        read_only_fields = fields
