from rest_framework.permissions import BasePermission

class IsSemesterAddRemove(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return hasattr(request.user, 'IsSemesterAddRemove')

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return hasattr(request.user, 'student')