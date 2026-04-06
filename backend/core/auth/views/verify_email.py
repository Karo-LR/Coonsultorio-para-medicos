from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.auth.utils import decode_email_verification_token


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"detail": "El token es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        user = decode_email_verification_token(token)
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response({"detail": "Correo verificado correctamente."}, status=status.HTTP_200_OK)
