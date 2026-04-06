from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.audit import log_event
from core.auth.serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if User.objects.exists():
            request_user = getattr(request, "user", None)
            request_role = getattr(getattr(request_user, "perfil", None), "rol", None)
            if not request_user or not request_user.is_authenticated or request_role != "admin":
                return Response(
                    {"detail": "El registro publico esta desactivado. Solo un administrador autenticado puede crear usuarios."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = RegisterSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        rol = getattr(user.perfil, "rol", "")
        is_initial_setup = User.objects.count() == 1 and rol == "admin"
        log_event(
            request,
            action="auth.user_created",
            instance=user,
            description="Usuario creado desde el flujo de registro controlado.",
            metadata={"rol": rol, "initial_setup": is_initial_setup},
        )
        return Response(
            {
                "detail": "Administrador inicial creado correctamente."
                if is_initial_setup
                else "Usuario creado correctamente.",
                "user_id": user.id,
                "email": user.email,
                "rol": rol,
            },
            status=status.HTTP_201_CREATED,
        )
