from rest_framework.permissions import BasePermission


class IsManagerOrSuperuser(BasePermission):
    """
    Allows access only to users who belong to the manager and superuser.
    """
    def has_permission(self, request, view):
        # Check if the user belongs to the 'Manager' group or superuser
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser


class IsCustomer(BasePermission):
    """
    Allows access only to customers (who do not belong) to any group.
    """

    def has_permission(self, request, view):
        # Check if the user does not belong to any group
        return not request.user.groups.exists()


class IsNotCustomer(BasePermission):
    """
    Allows access only to users who are not customers.
    """

    def has_permission(self, request, view):
        # Check if the user belongs to any group
        return request.user.groups.exists()
