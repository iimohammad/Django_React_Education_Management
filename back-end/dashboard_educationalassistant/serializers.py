from django.db import transaction
from rest_framework import serializers
from datetime import date

from accounts.models import Student, Teacher, User, EducationalAssistant
from education.models import (
                    Department,
                    Major,
                    Semester,
                    Course,
                    StudentCourse,
                    SemesterCourse,
                    SemesterUnitSelection,
                    SemesterClass,
                    SemesterAddRemove,
                    SemesterExam,
                    SemesterEmergency,
                    )
from dashboard_student.models import (
    EmergencyRemovalRequest,
    StudentDeleteSemesterRequest,
    EmploymentEducationRequest,
    SemesterRegistrationRequest,
    RevisionRequest,
    UnitSelectionRequest
)
from education.models import Department, Major, StudentCourse, SemesterCourse


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only = True)
    first_name = serializers.CharField(read_only = True)
    last_name = serializers.CharField(read_only = True)
    user_number = serializers.CharField(read_only = True)
    birthday = serializers.CharField(read_only = True)
    gender = serializers.CharField(read_only = True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'user_number',
            'national_code',
            'birthday',
            'profile_image',
            'phone',
            'address',
            'gender']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'department_code', 'year_established',
                  'department_location']


class SemesterUnitSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterUnitSelection
        fields = '__all__'


class SemesterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterClass
        fields = '__all__'


class SemesterAddRemoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterAddRemove
        fields = '__all__'


class SemesterExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterExam
        fields = '__all__'


class SemesterEmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterEmergency
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    unit_selection_time_range = SemesterUnitSelectionSerializer()
    class_time_range = SemesterClassSerializer()
    add_remove_time_range = SemesterAddRemoveSerializer()
    exams_time_range = SemesterExamSerializer()
    emergency_removal_time_range = SemesterEmergencySerializer()

    class Meta:
        model = Semester
        fields = ['id', 'name', 'start_semester', 'end_semester',
                  'semester_type', 'unit_selection_time_range',
                  'class_time_range', 'add_remove_time_range', 'exams_time_range',
                  'emergency_removal_time_range']
    
    def create(self, validated_data):
        unit_selection_time_range_data = validated_data.pop('unit_selection_time_range')
        class_time_range_data = validated_data.pop('class_time_range')
        add_remove_time_range_data = validated_data.pop('add_remove_time_range')
        exams_time_range_data = validated_data.pop('exams_time_range')
        emergency_removal_time_range_data = validated_data.pop('emergency_removal_time_range')

        semester = Semester.objects.create(**validated_data)

        SemesterUnitSelection.objects.create(semester=semester, **unit_selection_time_range_data)
        SemesterClass.objects.create(semester=semester, **class_time_range_data)
        SemesterAddRemove.objects.create(semester=semester, **add_remove_time_range_data)
        SemesterExam.objects.create(semester=semester, **exams_time_range_data)
        SemesterEmergency.objects.create(semester=semester, **emergency_removal_time_range_data)

        return semester


class MajorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Major
        fields = ['id', 'major_name', 'major_code', 'department',
                  'number_of_credits', 'level', 'education_group']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    major = MajorSerializer()

    class Meta:
        model = Student
        fields = [
            'id',
            'user',
            'entry_semester',
            'gpa',
            'entry_year',
            'major',
            'advisor',
            'military_service_status',
            'year_of_study',
        ]
    
    def get_fields(self):
        fields = super().get_fields()

        if self.context.get('request') and (self.context['request'].method == 'POST' 
                                            or self.context['request'].method == 'PUT'):
            educational_assistant = self.context['request'].user.educationalassistant

            fields['major'] = serializers.PrimaryKeyRelatedField(
                queryset=Major.objects.filter(
                    id=educational_assistant.field.id
                ))
            fields['advisor'] = serializers.PrimaryKeyRelatedField(
                queryset=Teacher.objects.filter(
                    department=educational_assistant.field.department
                ))
    
        return fields


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'expertise', 'rank', 'department']


class EducationalAssistantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    field = MajorSerializer(read_only = True)
    class Meta:
        model = EducationalAssistant
        fields = ['id', 'user', 'field']


class StudentCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='semester_course.course.course_name')
    semester_name = serializers.CharField(source='semester_course.semester.name')

    class Meta:
        model = StudentCourse
        fields = ['course_name', 'semester_name', 'status', 'score', 'is_pass']

class SemesterCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course_name')

    class Meta:
        model = StudentCourse
        fields = ['semester_course']

    def get_semester_course(self, obj):
        if obj.status == 'R' and obj.score == '':
            return obj.semester_course
        else:
            return None



        fields = ['id', 'user', 'expertise', 'rank', 'department']
    
    def get_fields(self):
        fields = super().get_fields()
        
        if self.context.get('request') and (self.context['request'].method == 'POST' 
                                            or self.context['request'].method == 'PUT'):
            educational_assistant = self.context['request'].user.educationalassistant

            fields['department'] = serializers.PrimaryKeyRelatedField(
                queryset=Department.objects.filter(
                    id=educational_assistant.field.department.id
                ))
    
        return fields


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_code', 'department',
                  'major', 'credit_num']
    
    def get_fields(self):
        fields = super().get_fields()

        if self.context.get('request') and (self.context['request'].method == 'POST' 
                                            or self.context['request'].method == 'PUT'):
            educational_assistant = self.context['request'].user.educationalassistant

            fields['department'] = serializers.PrimaryKeyRelatedField(
                queryset=Department.objects.filter(
                    id=educational_assistant.field.department.id
                ))
            fields['major'] = serializers.PrimaryKeyRelatedField(
                queryset=Major.objects.filter(
                    id=educational_assistant.field.id
                ))
    
        return fields


class SemesterCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterCourse
        fields = ['id', 'semester', 'course', 'class_days', 'class_time_start',
                  'class_time_end', 'exam_datetime', 'exam_location',
                  'instructor', 'course_capacity', 'corse_reserve_capasity']
        
    def get_class_days(self, obj):
        
        return [day.name for day in obj.class_days.all()]

    def get_fields(self):
        fields = super().get_fields()

        if self.context.get('request') and (self.context['request'].method == 'POST' 
                                            or self.context['request'].method == 'PUT'):
            educational_assistant = self.context['request'].user.educationalassistant

            fields['course'] = serializers.PrimaryKeyRelatedField(
                queryset=Course.objects.filter(
                    department=educational_assistant.field.department,
                    major=educational_assistant.field
                ))
            fields['instructor'] = serializers.PrimaryKeyRelatedField(
                queryset=Teacher.objects.filter(
                    department=educational_assistant.field.department
                ))
            fields['semester'] = serializers.PrimaryKeyRelatedField(
                queryset=Semester.objects.filter(
                    start_semester__lte=date.today(),
                    end_semester__gte=date.today()
                ))

        return fields


class EmergencyRemovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyRemovalRequest
        fields = ['id', 'student', 'approval_status', 'created_at',
                  'course', 'student_explanation']
        read_only_fields = ['id', 'student', 'created_at', 'course', 'student_explanation']
class SemesterRegistrationRequestSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']
        read_only_fields = ['name']

class SemesterRegistrationRequestSerializer(serializers.ModelSerializer):
    semester = SemesterRegistrationRequestSemesterSerializer()
    class Meta:
        model = SemesterRegistrationRequest
        fields = ['id','approval_status', 'created_at','semester' ]
        read_only_fields = ['id','approval_status', 'created_at' , 'semester',]
        
    

class StudentDeleteSemesterRequestSerializer(serializers.ModelSerializer):
    # semester_registration_request = SemesterRegistrationRequestSerializer()
    class Meta:
        model = StudentDeleteSemesterRequest
        fields = ['id', 'semester_registration_request', 'teacher_approval_status',
                  'educational_assistant_approval_status', 'created_at',
                  'student_explanations', 'educational_assistant_explanation']
        read_only_fields = ['id', 'semester_registration_request', 'teacher_approval_status',
                            'created_at', 'student_explanations']
        
    def update(self, instance, validated_data):
        if instance.educational_assistant_approval_status =='A' or \
                instance.educational_assistant_approval_status =='R':
            raise serializers.ValidationError('can not change answered request!')
        
        educational_assistant_explanation = validated_data.get('educational_assistant_explanation')
        educational_assistant_approval_status = validated_data.get('educational_assistant_approval_status')
        semester_registration_request = validated_data.get('semester_registration_request')
            # student_email = instance.semester_registration_request.student.user.email
        if educational_assistant_approval_status == 'A':
            try:
                with transaction.atomic():
                    instance.educational_assistant_explanation = educational_assistant_explanation
                    instance.educational_assistant_approval_status = educational_assistant_approval_status
                    semester = semester_registration_request.semester
                    student = semester_registration_request.student
                    StudentCourse.objects.filter(student = student,
                                                semester_course__semester = semester).update(status = 'S')
                    UnitSelectionRequest.objects.filter(
                        semester_registration_request = semester_registration_request).update(
                            approval_status = 'D')
                instance.save()
            except Exception as e:
                pass
            # send_semester_delete_approval_email.delay(student_email)
            
        elif educational_assistant_approval_status == 'R':
            try:
                instance.save()
            #   send_semester_delete_rejected_email.delay(student_email)
            except Exception as e:
                pass
        return instance
    
class EmploymentEducationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentEducationRequest
        fields = ['id', 'student', 'approval_status', 'created_at']
        read_only_fields = ['id', 'student', 'created_at']


class StudentCourseSerializer(serializers.ModelSerializer):
    semester_course = SemesterCourseSerializer()
    class Meta:
        model = StudentCourse
        fields = ['student', 'semester_course','status','score']


class RevisionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevisionRequest
        fields = ['id', 'student', 'teacher_approval_status',
                  'educational_assistant_approval_status', 'created_at',
                  'course', 'text', 'answer']
        read_only_fields = ['id', 'student', 'teacher_approval_status', 'created_at', 'course', 'text']
