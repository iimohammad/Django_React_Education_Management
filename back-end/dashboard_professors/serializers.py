from rest_framework import serializers

from dashboard_student.models import (
    AddRemoveRequest,
    EmergencyRemovalRequest,
    RevisionRequest,
    SemesterRegistrationRequest,
    StudentDeleteSemesterRequest,
    EmploymentEducationRequest,
)
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


class UnitSelectionRequestTeacherUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitSelectionRequest
        fields = ['id', 'approval_status']

    def validate_approval_status(self, value):
        if value not in UnitSelectionRequest.UnitSelection_APPROVAL_CHOICES:
            raise serializers.ValidationError("Invalid approval status.")
        return value

    def update(self, instance, validated_data):
        instance.approval_status = validated_data.get('approval_status', instance.approval_status)
        instance.save()
        return instance


class SemesterRegistrationConfirmationSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'student', 'approval_status', 'created_at', 'semester', 'requested_courses', 'teacher_comment_for_requested_courses']
        read_only_fields = ['id', 'student', 'created_at', 'semester', 'requested_courses']


    def update(self, instance, validated_data):
        instance.approval_status = validated_data.get('approval_status', instance.approval_status)
        instance.save()
        return instance

class AddRemoveRequestViewSerializers(UnitSelectionRequestTeacherUpdateSerializer):
    pass

class EmergencyRemovalConfirmationSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmergencyRemovalRequest
        fields = ['id', 'course', 'approval_status', 'created_at', 
                  'student_explanation', 'educational_assistant_explanation']
        
        read_only_fields = ['id', 'course', 'created_at', 'student_explanation', 'educational_assistant_explanation']

    def update(self, instance, validated_data):
        instance.approval_status = validated_data.get('approval_status', instance.approval_status)
        instance.save()
        return instance


class StudentDeleteSemesterRequestTeacherUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDeleteSemesterRequest
        fields = ['teacher_approval_status']

    def update(self, instance, validated_data):
        instance.teacher_approval_status = validated_data.get(
            'teacher_approval_status',
             instance.teacher_approval_status
             )
        instance.save()
        return instance




class RevisionRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = RevisionRequest
        fields = '__all__'


class EmploymentEducationConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentEducationRequest
        fields = ['id','approval_status','created_at','need_for']
        
        read_only_fields = ['id' ,'created_at','need_for']
        