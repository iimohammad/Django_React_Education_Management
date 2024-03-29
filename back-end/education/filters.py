from django_filters.rest_framework import FilterSet

from accounts.models import Student, Teacher


class StudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = {
            'user__username': ['exact'],
            'user__first_name': ['exact'],
            'user__last_name': ['exact'],
            'user__user_number': ['exact'],
            'user__national_code': ['exact'],
            'entry_year': ['exact', 'gte', 'lte'],
            'major__major_name': ['exact'],
            'year_of_study': ['exact', 'gte', 'lte'],
        }


class TeacherFilter(FilterSet):
    class Meta:
        model = Teacher
        fields = {
            'user__username': ['exact'],
            'user__first_name': ['exact'],
            'user__last_name': ['exact'],
            'user__user_number': ['exact'],
            'user__national_code': ['exact'],
            'rank': ['exact', 'gte', 'lte'],
            'department': ['exact'],
        }
