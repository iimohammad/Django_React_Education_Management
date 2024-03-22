from rest_framework.permissions import BasePermission

class IsEducationalAssistant(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        return hasattr(request.user, 'educationalassistant')
