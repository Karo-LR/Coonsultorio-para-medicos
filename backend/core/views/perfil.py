from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Perfil
from core.permissions import IsAdmin
from core.serializers import PerfilSerializer


class PerfilViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Perfil.objects.select_related("user").all()
    serializer_class = PerfilSerializer

    def get_permissions(self):
        if self.action == "me":
            return [IsAuthenticated()]
        return [IsAdmin()]

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user.perfil)
        return Response(serializer.data)
