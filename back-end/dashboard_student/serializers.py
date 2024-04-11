from rest_framework import serializers
from education.models import (
    Day,
    Major,
    Prerequisite,
    Requisite,
    SemesterClass,
    SemesterCourse,
    Semester,
    Department,
    Course,
    StudentCourse,
    Prerequisite,
    Requisite,
)
from accounts.models import Student, Teacher, User
from .models import (
    SemesterRegistrationRequest,
    RevisionRequest,
    EmergencyRemovalRequest,
    StudentDeleteSemesterRequest,
    EmploymentEducationRequest,
    AddRemoveRequest,
    EmploymentEducationRequest,
    UnitSelectionRequest,
    QueuedRequest,
)

from rest_framework.exceptions import NotFound
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Count

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name', 'department_code', 'year_established',
                  'department_location']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['user']


class SemesterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterClass
        fields = ['classes_start', 'classes_end']


class SemesterSerializer(serializers.ModelSerializer):
    classes = SemesterClassSerializer()

    class Meta:
        model = Semester
        fields = ['name', 'classes']

class CourseDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name']

class CourseMajortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['major_name']
        
class CourseSerializer(serializers.ModelSerializer):
    prerequisites = 'PrerequisiteSerializer()'
    required_by = 'RequisiteSerializer()'
    department = CourseDepartmentSerializer()
    major = CourseMajortSerializer()
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'credit_num', 'prerequisites', 'required_by',
                  'course_type' , 'department' , 'major']

class PrerequisiteSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Prerequisite
        fields = ['id', 'course', 'prerequisite']


class RequisiteSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Requisite
        fields = ['id', 'course', 'requisite']


class ClassDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['name']


class SemesterCourseSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    course = CourseSerializer()
    instructor = TeacherSerializer()
    class_days = ClassDaysSerializer(many=True, read_only=True)

    class Meta:
        model = SemesterCourse
        fields = ['semester', 'course', 'class_days', 'class_time_start', 'class_time_end',
                  'instructor', 'course_capacity', 'remain_course_capacity']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    advisor = TeacherSerializer()

    class Meta:
        model = Student
        fields = ['user', 'entry_semester', 'gpa', 'entry_year'
            , 'advisor', 'military_service_status', 'year_of_study', 'major']


class StudentCourseSerializer(serializers.ModelSerializer):
    semester_course = SemesterCourseSerializer()

    class Meta:
        model = StudentCourse
        fields = ['semester_course', 'status', 'score']


class ExamSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']


class ExamSemesterCourseSerializer(serializers.ModelSerializer):
    semester = ExamSemesterSerializer()
    course = CourseSerializer()

    class Meta:
        model = SemesterCourse
        fields = ['semester', 'course', 'exam_datetime', 'exam_location']


class ExamStudentCourseSerializer(serializers.ModelSerializer):
    semester_course = ExamSemesterCourseSerializer()

    class Meta:
        model = StudentCourse
        fields = ['semester_course']


class MajorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Major
        fields = ['major_name', 'major_code', 'level', 'education_group', 'department']


class ProfileStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    advisor = TeacherSerializer()
    major = MajorSerializer()

    class Meta:
        model = Student
        fields = ['user', 'entry_semester', 'gpa', 'entry_year'
            , 'advisor', 'military_service_status', 'year_of_study', 'major']


class SemesterRegistrationRequestSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']
        # read_only_fields = ['name']


class SemesterRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterRegistrationRequest
        fields = ['id', 'approval_status', 'created_at', 'semester', 'requested_courses', 'teacher_comment']
        read_only_fields = ['id', 'approval_status', 'created_at', 'teacher_comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'] = serializers.PrimaryKeyRelatedField(read_only=True,
                                            default=serializers.CurrentUserDefault())

    def validate(self, data):
        student = self.context['request'].user.student
        semester = data['semester']

        existing_requests = SemesterRegistrationRequest.objects.filter(
            student=student, semester=semester, approval_status__in=['P', 'A']
        ).exists()

        if existing_requests:
            raise serializers.ValidationError(
                "A request with 'P' or 'A' status already exists for this semester."
                )

        return data
class UnitselectionSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']

class UnitSelectionSemesterRegistrationRequestSerializer(serializers.ModelSerializer):
    semester = UnitselectionSemesterSerializer()
    class Meta:
        model = SemesterRegistrationRequest
        fields = ['semester']


class UnitSelectionRequestSerializer(serializers.ModelSerializer):
    semester_registration_request = UnitSelectionSemesterRegistrationRequestSerializer()
    request_course = SemesterCourseSerializer(many = True)

    class Meta:
        model = UnitSelectionRequest
        fields = ['id', 'semester_registration_request', 'approval_status',
                'created_at', 'request_course']

        read_only_fields = ['id', 'approval_status', 'created_at']

    def get_fields(self):
        fields = super().get_fields()
        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['request_course'] = serializers.PrimaryKeyRelatedField(
                queryset=SemesterCourse.objects.all())
            
            fields['semester_registration_request'] = serializers.PrimaryKeyRelatedField(
                queryset=SemesterRegistrationRequest.objects.all())

        return fields

    def create(self, validated_data):
        
        user = self.context['user']
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Invalid student")
        department = student.major.department
        
        semester_registration_request = validated_data.get('semester_registration_request')
        
        if semester_registration_request.student != student or semester_registration_request.approval_status != 'A':
            raise serializers.ValidationError("Invalid semester registration request")
        
        semester = semester_registration_request.semester
        
        
        current_date = timezone.now().date()
        
        if current_date < semester.unit_selection.unit_selection_start or \
                current_date > semester.unit_selection.unit_selection_end:
            raise serializers.ValidationError("Invalid semester unit selection time")
        
        
        request_course = validated_data.get('request_course')
        
        # check for none request_course
        if request_course == None:
            raise serializers.ValidationError("Invalid requested course")
        
        # check for request_course semester
        if request_course.semester != semester:
            raise serializers.ValidationError("Invalid requested course")
        
        # check for request_course department
        if request_course.course.department != department:
            raise serializers.ValidationError("Invalid requested course, course not in your department!")
        
        # check for exist of unit_selection_request
        unit_selection_request = UnitSelectionRequest.objects.filter(
                        semester_registration_request = semester_registration_request ,
                        ).first()
        
        # create unit_selection_request
        if unit_selection_request == None:
            try:
                unit_selection_request = UnitSelectionRequest.objects.create(
                        semester_registration_request = semester_registration_request ,
                        )
            except Exception as e:
                pass
            
        try:
            exists = unit_selection_request.request_course.filter(id=request_course.id).exists()
        except Exception as e:
            pass
        
        if exists or StudentCourse.objects.filter(
            semester_course = request_course ,
            student = student).exists():
            raise serializers.ValidationError("Course already requested!")
        
        try:
            prerequisite = request_course.course.required_by
        except Exception as e:
            pass
        
        requisite = request_course.course.required_with
        try:
            print('*************')
            print('requisite')
            print(requisite)
            print(Count(requisite))
            if Count(requisite)!=0:
                for requisite_course in requisite:
                    exists = UnitSelectionRequest.objects.filter(
                        semester_registration_request = semester_registration_request ,
                        request_course__course = requisite_course).exists()
                    if not exists:
                        raise serializers.ValidationError("The requisite is not met!")
        except Exception as e:
            print('*************')
            print('e')
            print(e)
            
        
        # if validated_data['request_course'].course_capacity == 0:
                # def create(self, request, *args, **kwargs):
            #     serializer = self.get_serializer(data=request.data)
            #     serializer.is_valid(raise_exception=True)
                
            #     if serializer.validated_data.get('request_course').course_capacity == 0:
            #         # Queue the request in Redis
            #         redis_conn = get_redis_connection('default')
            #         redis_conn.lpush('unit_selection_queue', json.dumps(serializer.validated_data))
                    
            #         # Send a message to the user
            #         messages.info(request, "Your request has been queued.")
            #         return Response({'detail': 'Your request has been queued.'}, status=status.HTTP_200_OK)
                
            #     return super().create(request, *args, **kwargs)
            # QueuedRequest.objects.create(
            #     student=student,
            #     **validated_data
            # )
            # raise ValidationError("Course capacity is zero, request is queued.")

        return unit_selection_request


class StudentDeleteSemesterRequestSerializer(serializers.ModelSerializer):
    semester_registration_request = UnitSelectionSemesterRegistrationRequestSerializer()
    class Meta:
        model = StudentDeleteSemesterRequest
        fields = ['id', 'semester_registration_request', 'teacher_approval_status',
                  'educational_assistant_approval_status', 'created_at',
                  'student_explanations', 'educational_assistant_explanation']

        read_only_fields = ['id', 'semester_registration_request', 'teacher_approval_status',
                            'educational_assistant_approval_status', 'created_at',
                            'educational_assistant_explanation']

    def get_fields(self):
        fields = super().get_fields()

        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['semester_registration_request'] = serializers.PrimaryKeyRelatedField(
                queryset=SemesterRegistrationRequest.objects.all())
        return fields

    def create(self, validated_data):
        semester_registration_request = validated_data.pop('semester_registration_request')
        user = self.context['user']
        semester = None
        try:
            semester_registration_request = StudentDeleteSemesterRequest.objects.get(
                pk=semester_registration_request.pk,
                student__user=user)
        except StudentDeleteSemesterRequest.DoesNotExist:
            raise serializers.ValidationError("Invalid SemesterRegistrationRequest")

        existing_request = StudentDeleteSemesterRequest.objects.filter(
            semester_registration_request=semester_registration_request,
            semester_registration_request__student__user=user).exists()
        if existing_request:
            raise serializers.ValidationError(
                "A unitselection request for this semester already exists")

        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Invalid student")

        semester = StudentDeleteSemesterRequest.objects.get(
            pk=semester_registration_request.pk).semester
        current_date = timezone.now().date()

        if (current_date < semester.start_semester or
                current_date > semester.end_semester
        ):
            raise serializers.ValidationError("Unvalide semester")

        student_delete_semester_request = StudentDeleteSemesterRequest.objects.create(
            semester_registration_request=semester_registration_request,
            student_explanations=validated_data.get('student_explanations')
        )
        return student_delete_semester_request


class RevisionRequestSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']


class RevisionRequestCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name']


class RevisionRequestStudentCourseSemesterCourseSerializer(serializers.ModelSerializer):
    course = RevisionRequestCourseSerializer()
    semester = RevisionRequestSemesterSerializer()

    class Meta:
        model = SemesterCourse
        fields = ['semester', 'course']


class RevisionRequestStudentCourseSerializer(serializers.ModelSerializer):
    semester_course = RevisionRequestStudentCourseSemesterCourseSerializer()

    class Meta:
        model = StudentCourse
        fields = ['semester_course', 'status', 'score']


class RevisionRequestSerializer(serializers.ModelSerializer):
    course = RevisionRequestStudentCourseSerializer()

    class Meta:
        model = RevisionRequest
        fields = ['id', 'course', 'educational_assistant_approval_status',
                  'teacher_approval_status', 'created_at', 'text', 'answer']

        read_only_fields = ['id', 'course', 'educational_assistant_approval_status',
                            'teacher_approval_status', 'created_at', 'answer']

    def get_fields(self):
        fields = super().get_fields()

        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['course'] = serializers.IntegerField()

        return fields

    def create(self, validated_data):
        student_course_pk = validated_data.get('course')
        user = self.context['user']

        try:
            student = Student.objects.get(user=user)
        except:
            raise serializers.ValidationError("Invalid student")

        try:
            course = StudentCourse.objects.get(pk=student_course_pk, student=student)
        except Exception:
            raise serializers.ValidationError("Invalid course")

        if course.score == None:
            raise serializers.ValidationError("Invalid course score")

        existing_request = RevisionRequest.objects.filter(
            course=course, student=student,
            teacher_approval_status='P',
            educational_assistant_approval_status='P').first()

        if existing_request != None:
            raise serializers.ValidationError(
                "A Revision request for this course already exists")
        validated_data['course'] = course
        revision_request = RevisionRequest.objects.create(
            student=student, course=course, text=validated_data['text'])

        return revision_request


class EmergencyRemovalRequestSerializer(serializers.ModelSerializer):
    course = StudentCourseSerializer()

    class Meta:
        model = EmergencyRemovalRequest
        fields = ['id', 'course', 'approval_status', 'created_at',
                  'student_explanation']

        read_only_fields = ['id', 'approval_status', 'created_at']

    def get_fields(self):
        fields = super().get_fields()

        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['course'] = serializers.IntegerField()

        return fields

    def create(self, validated_data):
        student_course_pk = validated_data.get('course')
        user = self.context['user']
        try:
            student = Student.objects.get(user=user)
        except:
            raise serializers.ValidationError("Invalid student")

        try:
            course = StudentCourse.objects.get(pk=student_course_pk, student=student)
        except Exception:
            raise serializers.ValidationError("Invalid course")

        current_date = timezone.now().date()
        emergency_start = course.semester_course.semester.emergency.emergency_remove_start
        emergency_end = course.semester_course.semester.emergency.emergency_remove_end

        if current_date < emergency_start:
            raise serializers.ValidationError("Emergency remove not accesible")
        elif current_date > emergency_end:
            raise serializers.ValidationError("Emergency remove ended")

        existing_request = EmergencyRemovalRequest.objects.filter(
            course=course, student=student, approval_status='P').first()

        if existing_request != None:
            raise serializers.ValidationError("A registration request for this semester already exists")

        validated_data['course'] = course
        try:
            emergency_removal_request = EmergencyRemovalRequest.objects.create(
                student=student, course=course,
                student_explanation=validated_data['student_explanation'])
        except Exception as e:
            print('*****************')
            print('*****************')
            print(validated_data)
            print(e)
        return emergency_removal_request


class AddRemoveRequestSerializer(UnitSelectionRequestSerializer):
    pass


class EmploymentEducationRequestSerializer(serializers.ModelSerializer):
    """
        Employment Education Request Serializer
    """

    class Meta:
        model = EmploymentEducationRequest
        fields = ['id', 'approval_status', 'created_at', 'need_for']

        read_only_fields = ['id', 'approval_status', 'created_at']

    def create(self, validated_data):
        user = self.context['user']
        try:
            student = Student.objects.get(user=user)
        except:
            raise serializers.ValidationError("Invalid student")

        existing_request = EmploymentEducationRequest.objects.filter(
            student=student, approval_status='P').first()

        if existing_request != None:
            raise serializers.ValidationError(
                "A registration request for this semester already exists")

        employment_education_request = EmploymentEducationRequest.objects.create(
            student=student,
            need_for=self.validated_data.get('need_for')
        )

        return employment_education_request
