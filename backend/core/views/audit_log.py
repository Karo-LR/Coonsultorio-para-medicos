from rest_framework import filters, viewsets

from core.models import AuditLog
from core.permissions import IsAdmin
from core.serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("actor").all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at", "action", "resource_type"]
    search_fields = ["action", "resource_type", "resource_repr", "description", "actor__username"]
