from rest_framework import serializers

from .models import Course, Department, Semester, SemesterCourse, StudentCourse


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class SemesterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class SemesterCourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = SemesterCourse
        fields = '__all__'


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['id', 'student', 'semester_course', 'status', 'score']

