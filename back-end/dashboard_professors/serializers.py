from rest_framework import serializers

from education.models import Course, Semester, SemesterCourse


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name']


class SemesterCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course_name')

    class Meta:
        model = SemesterCourse
        fields = ['id', 'course_name']
        # readonly_fields = ['id', 'course_name']


class ShowSemestersSerializers(serializers.ModelSerializer):
    Semester_courses = SemesterCourseSerializer(many=True, read_only=True)

    class Meta:
        model = Semester
        fields = ['id', 'name', 'start_semester',
                  'end_semester', 'semester_type', 'Semester_courses']
