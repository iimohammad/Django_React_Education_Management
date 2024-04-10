from rest_framework.permissions import BasePermission
from accounts.models import Teacher
class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return hasattr(request.user, 'teacher')
    
class IsAdvisor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return Teacher.objects.get(user = request.user).can_be_advisor
        