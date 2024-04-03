from rest_framework.permissions import BasePermission
from accounts.models import Student
from education.models import Semester
from .models import SemesterRegistrationRequest

class IsEducationalAssistant(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return hasattr(request.user, 'educationalassistant')


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return hasattr(request.user, 'student')
    
class HavePermosionForUnitSelectionForLastSemester(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        student = Student.objects.get(user = request.user)
        
        last_semester = Semester.objects.order_by('-start_semester').first()
        return SemesterRegistrationRequest.objects.filter(
            semester = last_semester,
            student = student,
            approval_status = 'A').exists()
