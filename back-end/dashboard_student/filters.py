from django_filters.rest_framework import FilterSet

from education.models import SemesterCourse, StudentCourse, Course


class SemesterCourseFilter(FilterSet):
    class Meta:
        model = SemesterCourse
        fields = {
            'semester__name': ['contains'],
            'course__course_name': ['contains'],
        }


class StudentCourseFilter(FilterSet):
    class Meta:
        model = StudentCourse
        fields = {
            'semester_course__course__course_name': ['contains'],
            'semester_course__semester__name': ['contains'],

            'status': ['exact'],
        }


class StudentExamFilter(FilterSet):
    class Meta:
        model = StudentCourse
        fields = {
            'semester_course__course__course_name': ['contains'],
            'semester_course__semester__name': ['contains'],
        }


class CorseFilter(FilterSet):
    class Meta:
        model = Course
        fields = {
            'course_type': ['exact'],
            'course_name': ['contains'],
        }
