from rest_framework.permissions import BasePermission


def get_user_role(user):
    perfil = getattr(user, "perfil", None)
    return getattr(perfil, "rol", None)


class RolePermission(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return get_user_role(request.user) in self.allowed_roles


class IsAdmin(RolePermission):
    allowed_roles = ["admin"]


class IsDoctor(RolePermission):
    allowed_roles = ["doctor"]


class IsRecepcion(RolePermission):
    allowed_roles = ["recepcionista"]


class IsAdminOrDoctor(RolePermission):
    allowed_roles = ["admin", "doctor"]


class IsAdminOrRecepcion(RolePermission):
    allowed_roles = ["admin", "recepcionista"]


class IsStaffRole(RolePermission):
    allowed_roles = ["admin", "doctor", "recepcionista"]
