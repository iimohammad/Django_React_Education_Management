from rest_framework import serializers

from dashboard_student.models import AddRemoveRequest, EmergencyRemovalRequest, EnrollmentRequest, RevisionRequest, SemesterRegistrationRequest, StudentDeleteSemesterRequest
from education.models import Course, Major, Semester, SemesterCourse , StudentCourse
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


class UnitSelectionRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = UnitSelectionRequest
        fields = ['semester_registration_request' , 'approval_status' ,'created_at' , 'requested_courses']
        read_only_fields = ['semester_registration_request' ,'created_at' , 'requested_courses']

class SemesterSerializerName(serializers.ModelSerializer):
    class Meta:
        model = Semester()
        fields = ['name']
class SemesterRegistrationRequestSerializers(serializers.ModelSerializer):
    student = StudentSerializerNameLastname()
    semester = SemesterSerializerName()
    requested_courses = CourseSerializer(many = True)
    class Meta:
        model = SemesterRegistrationRequest
        fields = ['student' ,'approval_status' ,'created_at' ,'semester' ,'requested_courses' ,
                    'student_comment_for_requested_courses']
        read_only_fields = ['student' ,'created_at' ,'semester' ,'requested_courses']


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