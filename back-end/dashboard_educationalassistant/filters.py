from django_filters.rest_framework import FilterSet, CharFilter

from accounts.models import Student, Teacher
from education.models import Course, SemesterCourse, StudentCourse
from dashboard_student.models import (
    EmergencyRemovalRequest,
    StudentDeleteSemesterRequest,
    EmploymentEducationRequest,
    RevisionRequest,
)


class StudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = {
            'user__username': ['contains'],
            'user__first_name': ['contains'],
            'user__last_name': ['contains'],
            'user__user_number': ['exact'],
            'user__national_code': ['exact'],
            'entry_year': ['exact', 'gte', 'lte'],
            'major__major_name': ['contains'],
            'major__department__department_name': ['contains'],
            'military_service_status': ['exact'],
        }


class TeacherFilter(FilterSet):
    class Meta:
        model = Teacher
        fields = {
            'user__username': ['contains'],
            'user__first_name': ['contains'],
            'user__last_name': ['contains'],
            'user__user_number': ['exact'],
            'user__national_code': ['exact'],
            'rank': ['exact', 'gte', 'lte'],
            'department__department_name': ['contains'],
        }


class CourseFilter(FilterSet):
    class Meta:
        model = Course 
        fields = {
            'department__department_name': ['contains'],
            'major__major_name': ['contains'],
            'credit_num': ['exact', 'gte', 'lte'],
        }


class SemesterCourseFilter(FilterSet):
    class_days = CharFilter(field_name='class_days__name', lookup_expr='exact')

    class Meta:
        model = SemesterCourse
        fields = {
            'semester__name': ['contains'],
            'course__course_name': ['contains'],
            'class_time_start': ['gte', 'lte'],
            'class_time_end': ['gte', 'lte'],
            'exam_datetime': ['gte', 'lte'],
            'instructor__user__username': ['contains'],
            'instructor__user__first_name': ['contains'],
            'instructor__user__last_name': ['contains'],
            'course_capacity': ['exact', 'gte', 'lte'],
            'corse_reserve_capasity': ['gte'],
            'class_days': ['exact'],
        }


class EmergencyRemovalRequestFilter(FilterSet):
    class Meta:
        model = EmergencyRemovalRequest
        fields = {
            'student__user__first_name': ['contains'],
            'student__user__last_name': ['contains'],
            'created_at': ['gte', 'lte'],
            'course__semester_course__course__course_name': ['contains'],
            'student_explanation': ['contains'],
        }


class StudentDeleteSemesterRequestFilter(FilterSet):
    class Meta:
        model = StudentDeleteSemesterRequest
        fields = {
            'semester_registration_request__student__user__first_name': ['contains'],
            'semester_registration_request__student__user__last_name': ['contains'],
            'semester_registration_request__semester__name': ['contains'],
            'created_at': ['gte', 'lte'],
            'student_explanations': ['contains'],
            'educational_assistant_explanation': ['contains'],
        }


class EmploymentEducationRequestFilter(FilterSet):
    class Meta:
        model = EmploymentEducationRequest
        fields = {
            'student__user__first_name': ['contains'],
            'student__user__last_name': ['contains'],
            'created_at': ['gte', 'lte'],
        }


class StudentCourseFilter(FilterSet):
    class Meta:
        model = StudentCourse
        fields = {
            'semester_course__course__course_name': ['contains'],
            'semester_course__semester__name': ['contains'],
            'student__user__national_code': ['exact'],
            'student__user__user_number': ['exact'],
            'status': ['exact'],
        }


class RevisionRequestFilter(FilterSet):
    class Meta:
        model = RevisionRequest
        fields = {
            'student__user__first_name': ['contains'],
            'student__user__last_name': ['contains'],
            'created_at': ['gte', 'lte'],
            'course__semester_course__course__course_name': ['contains'],
        }