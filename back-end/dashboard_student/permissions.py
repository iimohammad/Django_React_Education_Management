from rest_framework.permissions import BasePermission
from accounts.models import Student
from education.models import Semester, SemesterAddRemove, SemesterUnitSelection
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

class HavePermissionBasedOnUnitSelectionTimeORaddremoveTime(BasePermission):
    def has_permission(self, request, view):
        current_date = timezone.now().date()

        try:
            semester = Semester.objects.order_by('-start_semester').first()
            semester_registration_request = SemesterRegistrationRequest.objects.get(
                semester = semester ,
                student__user = request.user ,
                approval_status = 'A'
                )
        except SemesterRegistrationRequest.DoesNotExist:
            return False

        semester = semester_registration_request.semester
        
        if (
            current_date < semester.unit_selection.unit_selection_start or
            current_date > semester.unit_selection.unit_selection_end
        ):
            unit_selection_permission =  False
        else:
            unit_selection_permission = True
        
        if (
            current_date < semester.addremove.addremove_start or
            current_date > semester.addremove.addremove_end
        ):
            addremove_permission =  False
        else:
            addremove_permission = True
        return (addremove_permission or unit_selection_permission)

from rest_framework.permissions import BasePermission
from django.utils import timezone
from .models import SemesterRegistrationRequest

class HavePermissionBasedOnAddAndRemoveTime(BasePermission):
    def has_permission(self, request, view):
        current_date = timezone.now().date()

        try:
            semester_registration_request_id = request.data.get('semester_registration_request')
            if not semester_registration_request_id:
                return False
            
            semester_registration_request = SemesterRegistrationRequest.objects.get(pk=semester_registration_request_id)
            add_remove_period = semester_registration_request.semester.addremove
            if (
                current_date < add_remove_period.addremove_start or
                current_date > add_remove_period.addremove_end
            ):
                return False
        except (SemesterRegistrationRequest.DoesNotExist, SemesterAddRemove.DoesNotExist):
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
            if student.military_service_status == 'F':
                return False
        return True
    

