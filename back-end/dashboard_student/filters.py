from django_filters.rest_framework import FilterSet
from education.models import SemesterCourse , StudentCourse

class SemesterCourseFilter(FilterSet):
  class Meta:
    model = SemesterCourse
    fields = {
            'semester__name': ['exact'],
            'course__course_name': ['exact'],
    }
    
class StudentCourseFilter(FilterSet):
  class Meta:
    model = StudentCourse
    fields = {
            # 'course__course_name': ['exact'],
            'student__user__username': ['exact'],
            'student__user__first_name': ['exact'],
            'student__user__last_name': ['exact'],
            'status': ['exact'],
    }