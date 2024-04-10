from rest_framework import serializers
from .tasks import (
    send_approval_email, 
    send_rejection_email,
    send_unit_selection_email,
    send_semester_delete_approval_email,
    send_semester_delete_rejected_email,
    send_rejected_revision,
    send_approved_revision,
    
    )

from dashboard_student.models import (
    AddRemoveRequest,
    EmergencyRemovalRequest,
    RevisionRequest,
    SemesterRegistrationRequest,
    StudentDeleteSemesterRequest,
    EmploymentEducationRequest,
)
from education.models import Course, Semester, SemesterCourse,Major,StudentCourse
from dashboard_student.models import (
    UnitSelectionRequest,
    
    )
from accounts.models import Student , User
class UserSerializerNameLastname(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
    
class MajorSerializerName(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['major_name']
        
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializerNameLastname()
    major = MajorSerializerName()
    class Meta:
        model = Student
        fields = ['id', 'user', 'entry_semester', 'gpa', 'entry_year', 'major',
                    'military_service_status','year_of_study']
class StudentSerializerNameLastname(serializers.ModelSerializer):
    user = UserSerializerNameLastname() 
    class Meta:
        model = Student
        fields = ['user']
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name']


class SemesterCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course_name')

    class Meta:
        model = SemesterCourse
        fields = ['id', 'course_name']
        read_only_fields = ['id', 'course_name']


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

        student_email = instance.student.user.email
        send_unit_selection_email.delay(student_email, instance.approval_status)
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
        student_courses = StudentCourse.objects.filter(
            course=instance.course, 
            student=instance.student
        )
        for student_course in student_courses:
            if instance.approval_status == 'A':
                send_DeleteCourse_email.delay(instance.student.user.email)
            elif instance.approval_status == 'R':
                send_Reject_DeleteCourse_email.delay(instance.student.user.email)

        return instance

class StudentDeleteSemesterRequestTeacherUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDeleteSemesterRequest
        fields = ['teacher_approval_status']

    def update(self, instance, validated_data):
        teacher_approval_status = validated_data.get('teacher_approval_status', instance.teacher_approval_status)
        student_email = instance.semester_registration_request.student.user.email

        if teacher_approval_status == 'A':  
            send_semester_delete_approval_email.delay(student_email)

        elif teacher_approval_status == 'R':
            send_semester_delete_rejected_email.delay(student_email)

        instance.teacher_approval_status = teacher_approval_status
        instance.save()
        return instance



class studentCourseSerializer(serializers.ModelSerializer):
    semester_course = SemesterCourseSerializer()
    class Meta:
        model = StudentCourse
        fields = ['semester_course']


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
        if instance.teacher_approval_status == 'A':
            send_approved_revision.delay(instance.student.user.email)
        elif instance.teacher_approval_status == 'R':
            send_rejected_revision.delay(instance.student.user.email)

        return instance

class EmploymentEducationConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentEducationRequest
        fields = ['id','approval_status','created_at','need_for']
        
        read_only_fields = ['id' ,'created_at','need_for']



class SemesterRegistrationRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = SemesterRegistrationRequest
        fields = ['id', 'student', 'approval_status', 'created_at', 
                  'semester', 'requested_courses', 'teacher_comment_for_requested_courses']
        read_only_fields = ['id', 'student', 'created_at', 'semester', 'requested_courses']
        
    def validate_approval_status(self, value):
        if value not in ['P', 'A', 'R']:
            raise serializers.ValidationError("Invalid approval status.")
        return value

    def update(self, instance, validated_data):
        previous_status = instance.approval_status
        instance.approval_status = validated_data.get(
            'approval_status',
            instance.approval_status)

        instance.teacher_comment_for_requested_courses = validated_data.get(
            'teacher_comment_for_requested_courses',
             instance.teacher_comment_for_requested_courses
             )
        instance.save()
        
        if previous_status != instance.approval_status:
            if instance.approval_status == 'A':
                send_approval_email.delay(instance.student.user.email)
            elif instance.approval_status == 'R':
                send_rejection_email.delay(instance.student.user.email)
        
        return instance