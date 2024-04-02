from rest_framework import serializers

from dashboard_student.models import AddRemoveRequest, EmergencyRemovalRequest, EnrollmentRequest, RevisionRequest, SemesterRegistrationRequest, StudentDeleteSemesterRequest
from education.models import Course, Semester, SemesterCourse
from dashboard_student.models import (
    UnitSelectionRequest,
    )

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


class UnitSelectionRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = UnitSelectionRequest
        fields = '__all__'


class SemesterRegistrationRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = SemesterRegistrationRequest
        fields = '__all__'


class AddRemoveRequestViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = AddRemoveRequest
        fields = '__all__'

class EmergencyRemovalRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmergencyRemovalRequest
        fields = '__all__'


class StudentDeleteSemesterRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentDeleteSemesterRequest
        fields = '__all__'


class EnrollmentRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentRequest
        fields = '__all__'


class RevisionRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = RevisionRequest
        fields = '__all__'