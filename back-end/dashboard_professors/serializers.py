from rest_framework import serializers

from dashboard_student.models import AddRemoveRequest, EmergencyRemovalRequest, EnrollmentRequest, RevisionRequest, SemesterRegistrationRequest, StudentDeleteSemesterRequest
from education.models import Course, Semester, SemesterCourse , StudentCourse
from dashboard_student.models import (
    UnitSelectionRequest,
    )
from accounts.models import Student , User

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
        fields = ['semester_registration_request' , 'approval_status' ,'created_at' , 'requested_courses']
        read_only_fields = ['semester_registration_request' ,'created_at' , 'requested_courses']


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

class studentCourseSerializer(serializers.ModelSerializer):
    semester_course = SemesterCourseSerializer()
    class Meta:
        model = StudentCourse
        fields = ['semester_course']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name' ,'last_name']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Student
        fields = ['user']
class RevisionRequestSerializers(serializers.ModelSerializer):
    student = StudentSerializer()
    course = studentCourseSerializer()
    class Meta:
        model = RevisionRequest
        fields = ['id' , 'student', 'teacher_approval_status', 'educational_assistant_approval_status',
                    'created_at', 'course', 'text' , 'answer']
        
        read_only_fields = ['id' , 'student', 'educational_assistant_approval_status',
                    'created_at', 'text']
        
    def update(self, instance, validated_data):
        instance.teacher_approval_status = validated_data.get(
            'teacher_approval_status', instance.teacher_approval_status)
        instance.answer = validated_data.get('answer', instance.answer)
        instance.save()
        return instance