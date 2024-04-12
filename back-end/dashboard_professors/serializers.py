from rest_framework import serializers
from django.utils import timezone
import decimal
from .tasks import (
    send_approval_email, 
    send_rejection_email,
    send_unit_selection_email,
    send_semester_delete_approval_email,
    send_semester_delete_rejected_email,
    send_rejected_revision,
    send_approved_revision,
    
    )
import csv
from rest_framework import status
from rest_framework.response import Response

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

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']
        read_only_fields = ['name']
class SemesterRegistrationConfirmationSerializers(serializers.ModelSerializer):
    student = StudentSerializerNameLastname()
    semester = SemesterSerializer()
    class Meta:
        model = SemesterRegistrationRequest
        fields = ['id','student', 'approval_status', 'created_at', 'semester']
        read_only_fields = ['id', 'student', 'created_at', 'semester']


    def update(self, instance, validated_data):
        instance.approval_status = validated_data.get('approval_status', instance.approval_status)
        instance.save()
        return instance

class AddRemoveRequestViewSerializers(UnitSelectionRequestTeacherUpdateSerializer):
    pass


class StudentCourseSerializer(serializers.ModelSerializer):
    semester_course = SemesterCourseSerializer()
    class Meta:
        model = StudentCourse
        fields = ['semester_course','status','score']

class EmergencyRemovalConfirmationSerializers(serializers.ModelSerializer):
    student = StudentSerializerNameLastname(read_only=True)
    course = StudentCourseSerializer(read_only=True)
    class Meta:
        model = EmergencyRemovalRequest
        fields = ['id','student' ,'course', 'approval_status', 'created_at', 
                    'student_explanation']
        
        read_only_fields = ['id','student' , 'course', 'created_at', 'student_explanation']
    
    
    def update(self, instance, validated_data):
        
        if instance.approval_status == 'A' or instance.approval_status == 'R':
            raise serializers.ValidationError('cat not change Accepted   and rejected request!')
        
        instance.approval_status = validated_data.get('approval_status', instance.approval_status)
        
        if instance.approval_status == 'R':
            instance.save()
        
        elif instance.approval_status == 'A':
            course = instance.course
            
            end_semester = course.semester_course.semester.end_semester
            
            if end_semester < timezone.now().date():
                raise serializers.ValidationError('semester ended!')
            
            course.status = 'E'
            try:
                course.save()
            except Exception as e:
                pass
            instance.save()
            
        return instance

class StudentDeleteSemesterRequestTeacherSerializer(serializers.ModelSerializer):
    # semester_registration_request = SemesterRegistrationConfirmationSerializers()
    class Meta:
        model = StudentDeleteSemesterRequest
        fields = ['id' ,'semester_registration_request','teacher_approval_status' , 'created_at' ,
                    'student_explanations']
        read_only_fields = ['id' ,'semester_registration_request', 'created_at' ,
                    'student_explanations']
        
    def update(self, instance, validated_data):
        if instance.teacher_approval_status == 'A' or instance.teacher_approval_status == 'R' or \
            instance.educational_assistant_approval_status =='A' or \
                instance.educational_assistant_approval_status =='R':
            raise serializers.ValidationError('can not change answered request!')
        
        teacher_approval_status = validated_data.get('teacher_approval_status')
        if teacher_approval_status == 'A' or teacher_approval_status == 'R':
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
class MajorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Major
        fields = ['major_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','user_number']
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    major = MajorSerializer()

    class Meta:
        model = Student
        fields = [
            'user',
            'major',
        ]
class RevisionRequeststudentCourseSerializer(serializers.ModelSerializer):
    semester_course = SemesterCourseSerializer()
    class Meta:
        model = StudentCourse
        fields = ['semester_course' , 'status' , 'score']
class RevisionRequestSerializers(serializers.ModelSerializer):
    student = StudentSerializer()
    course = RevisionRequeststudentCourseSerializer()
    class Meta:
        model = RevisionRequest
        fields = ['id' , 'student', 'teacher_approval_status', 'educational_assistant_approval_status',
                    'created_at', 'course', 'text' , 'answer' , 'score']
        
        read_only_fields = ['id' , 'student', 'educational_assistant_approval_status',
                    'created_at', 'text']
        

    def update(self, instance, validated_data):
        if instance.educational_assistant_approval_status != 'P' or \
            instance.teacher_approval_status != 'P':
            raise serializers.ValidationError('can not modify answered request')
        
        instance.teacher_approval_status = validated_data.get(
            'teacher_approval_status', instance.teacher_approval_status)
        
        instance.answer = validated_data.get('answer', instance.answer)
        if instance.teacher_approval_status == 'A':
            score = validated_data.get('score')
            try:
                score = decimal.Decimal(score)
            except Exception as e:
                raise serializers.ValidationError('invalid score!')
            if score>20 or score<0:
                raise serializers.ValidationError('invalid score!')
            instance.score =score
            send_approved_revision.delay(instance.student.user.email)
        elif instance.teacher_approval_status == 'R':
            send_rejected_revision.delay(instance.student.user.email)

        instance.save()
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
                  'semester', 'requested_courses', 'teacher_comment']
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

        instance.teacher_comment = validated_data.get(
            'teacher_comment',
             instance.teacher_comment
             )
        instance.save()
        
        if previous_status != instance.approval_status:
            if instance.approval_status == 'A':
                send_approval_email.delay(instance.student.user.email)
            elif instance.approval_status == 'R':
                send_rejection_email.delay(instance.student.user.email)
        
        return instance
    

class EvaluationSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['id', 'semester_course','student',  'status', 'score']
        read_only_fields = ['id','status']
    

class CSVFileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        file_obj = validated_data.get('file')

        if not file_obj:
            raise serializers.ValidationError("No file uploaded")

        try:
            decoded_file = file_obj.read().decode('utf-8').splitlines()
            csv_data = csv.DictReader(decoded_file)

            for row in csv_data:
                student_id = row.get('student_id')
                score = row.get('score')

                if not student_id or not score:
                    raise serializers.ValidationError("Both student_id and score are required.")

                student_course = StudentCourse.objects.filter(student_id=student_id).first()
                if student_course:
                    student_course.score = score
                    student_course.save()

            return {'message': 'Student scores updated successfully'}

        except Exception as e:
            raise serializers.ValidationError("An error occurred while processing the CSV file")