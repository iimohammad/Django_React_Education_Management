from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return hasattr(request.user, 'teacher')


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return hasattr(request.user, 'student')


class IsEducationalAssistant(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return hasattr(request.user, 'educationalassistant')


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return hasattr(request.user, 'adminuser')



class IsNotAuthenticated(BasePermission):
    """
    Custom permission to only allow access to unauthenticated users.
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated