from rest_framework.permissions import BasePermission
from accounts.models import Student
from education.models import Semester, SemesterUnitSelection
from .models import SemesterRegistrationRequest,AddRemoveRequest
from django.utils import timezone


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

class HavePermissionBasedOnUnitSelectionTime(BasePermission):
    def has_permission(self, request, view):
        current_date = timezone.now().date()

        try:
            semester_registration_request = SemesterRegistrationRequest.objects.get(
                pk=request.data['semester_registration_request']
                )
        except SemesterRegistrationRequest.DoesNotExist:
            return False

        if (
            current_date < semester_registration_request.semester.unit_selection.unit_selection_start or
            current_date > semester_registration_request.semester.unit_selection.unit_selection_end
        ):
            return False
        
        return True


class HavePermissionBasedOnAddAndRemoveTime(BasePermission):
    def has_permission(self, request, view):
        current_date = timezone.now().date()

        try:
            add_remove_request_id = request.data.get('semester_registration_request')
            if not add_remove_request_id:
                return False
            
            add_remove_request = AddRemoveRequest.objects.get(pk=add_remove_request_id)
            add_remove_period = add_remove_request.semester_registration_request.semester.addremove
            if (
                current_date < add_remove_period.addremove_start or
                current_date > add_remove_period.addremove_end
            ):
                return False
        except (AddRemoveRequest.DoesNotExist, SemesterAddRemove.DoesNotExist):
            return False

        return True
        
class HavePermssionBasedOnEmergencyRemoveTime(BasePermission):
    pass


class HavePermssionBasedOnDeleteSemesterRequestTime(BasePermission):
    pass


class HavePermssionEmoloymentDegreeTime(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and hasattr(request.user, 'student'):
            student = request.user.student
            if student.military_service_status != 'F':
                return False
        return True
    

