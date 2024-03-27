from django_filters.rest_framework import FilterSet
from accounts.models import Student , Teacher

class StudentFilter(FilterSet):
  class Meta:
    model = Student
    fields = {
            'user__username': ['contains'],
            'user__first_name': ['contains'],
            'user__last_name': ['contains'],
            'user__user_number':['exact'],
            'user__national_code':['exact'],
            'entry_year': ['exact', 'gte', 'lte'],
            'major__major_name': ['contains'],
        }
    
    
class TeacherFilter(FilterSet):
  class Meta:
    model = Teacher
    fields = {
            'user__username': ['contains'],
            'user__first_name': ['contains'],
            'user__last_name': ['contains'],
            'user__user_number':['exact'],
            'user__national_code':['exact'],
            'rank': ['exact', 'gte', 'lte'],
            'department__department_name': ['contains'],
        }