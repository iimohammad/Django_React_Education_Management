from django.db.models import Q
from rest_framework import serializers , response , status
from dashboard_student.utils import add_from_redis_to_database, find_remain_credit, save_to_redis
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
    SemesterEmergency,
    StudentCourse,
    Prerequisite,
    Requisite,
)
from django.db import transaction
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
        
class PrerequisiteRequisiteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'credit_num']
class PrerequisiteSerializer(serializers.ModelSerializer):
    prerequisite = PrerequisiteRequisiteCourseSerializer()
    class Meta:
        model = Prerequisite
        fields = ['prerequisite']

class RequisiteSerializer(serializers.ModelSerializer):
    requisite = PrerequisiteRequisiteCourseSerializer()

    class Meta:
        model = Requisite
        fields = ['requisite']

class CourseSerializer(serializers.ModelSerializer):
    required_by = PrerequisiteSerializer(many=True)
    required_with = RequisiteSerializer(many=True)
    department = CourseDepartmentSerializer()
    major = CourseMajortSerializer()
    class Meta:
        model = Course
        fields = ['id' ,'course_name', 'course_code', 'credit_num', 'required_by', 'required_with',
                  'course_type' , 'department' , 'major']



class ClassDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['name']


class SemesterCourseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'credit_num',
                  'course_type']
class SemesterCourseSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    course = SemesterCourseCourseSerializer()
    instructor = TeacherSerializer()
    class_days = ClassDaysSerializer(many=True, read_only=True)

    class Meta:
        model = SemesterCourse
        fields = ['id','semester', 'course', 'class_days', 'class_time_start', 'class_time_end',
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
        fields = ['id','semester_course', 'status', 'score']


class ExamSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']


class ExamSemesterCourseSerializer(serializers.ModelSerializer):
    semester = ExamSemesterSerializer()
    course = SemesterCourseCourseSerializer()

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
    requested_courses = SemesterCourseCourseSerializer(many = True)
    semester = SemesterSerializer()
    class Meta:
        model = SemesterRegistrationRequest
        fields = ['id', 'approval_status', 'created_at', 'semester', 'requested_courses', 'teacher_comment']
        read_only_fields = ['id', 'approval_status', 'created_at', 'teacher_comment']


    def get_fields(self):
        fields = super().get_fields()
        if self.context.get('request') and (self.context['request'].method == 'POST'):
            fields.pop('semester')
            fields['requested_courses'] = serializers.PrimaryKeyRelatedField(
                queryset = Course.objects.all() , many = True)
        return fields
    def create(self, validated_data):
        student = self.context['request'].user.student
        
        semester = Semester.objects.order_by('-start_semester').first()

        existing_requests = SemesterRegistrationRequest.objects.filter(
            student=student, semester=semester, approval_status__in=['P', 'A']
        ).exists()

        if existing_requests:
            raise serializers.ValidationError(
                "A request with 'P' or 'A' status already exists for this semester."
                )

        semester_registration_request = SemesterRegistrationRequest.objects.create(
                            student = student ,
                            semester = semester ,
                            ).requested_courses.set(validated_data['requested_courses'])
        # return semester_registration_request
        
        return response.Response(
            data={'message': 'request createed'},
            status=status.HTTP_201_CREATED
            )
    
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
    request_course = SemesterCourseSerializer()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request') and self.context['request'].method == 'POST':
            self.fields['approval_status'].default = 'A'
    class Meta:
        model = UnitSelectionRequest
        fields = ['id', 'semester_registration_request', 'approval_status',
                  'created_at', 'request_course']
        read_only_fields = ['id', 'created_at', 'approval_status']
    def get_fields(self):
        fields = super().get_fields()
        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['request_course'] = serializers.PrimaryKeyRelatedField(
                queryset = SemesterCourse.objects.all()
            )
            # fields['semester_registration_request'] = serializers.PrimaryKeyRelatedField(
            #     queryset = SemesterRegistrationRequest.objects.all()
            # )
            fields.pop('semester_registration_request')
            
        return fields
    def create(self, validated_data):
        user = self.context['user']
        student = Student.objects.get(user=user)
        department = student.major.department
        # print(gpa_catergory(student.gpa))
        # semester_registration_request = validated_data.get('semester_registration_request')
        # if semester_registration_request.student != student:
        #     raise serializers.ValidationError("wrong semester registration request")
        # semester = semester_registration_request.semester

        semester = Semester.objects.order_by('-start_semester').first()
        try:
            semester_registration_request = SemesterRegistrationRequest.objects.get(
                semester = semester ,
                student = student ,
                approval_status = 'A')
        except:
            raise serializers.ValidationError("wrong semester registration request")
        request_course = validated_data.get('request_course')
        
        if request_course.semester != semester:
            raise serializers.ValidationError("invalid course")
        
        try:
            remain_credit = find_remain_credit(student)
        except Exception as e:
            pass
        if remain_credit==0 or request_course.course.credit_num > remain_credit:
            raise serializers.ValidationError("You can not add more courses")

        # check course capacity
        remain_capacity = request_course.remain_course_capacity
        if remain_capacity == 0:
            # Save request to Redis
            save_to_redis(validated_data.get('request_course').id, user.id)
            raise serializers.ValidationError(
                "You cannot add course because the course capacity is full but is reserved for you"
                )
        
        # check for request_course department
        course_department = request_course.course.department

        if course_department != department:
            raise serializers.ValidationError(
                "Invalid requested course, course not in your department!"
            )
        
        basic_course = request_course.course
        # #Prerequisite
        
        try:
            prerequisite = Prerequisite.objects.filter(course = basic_course)
        except Exception as e:
            pass
        for prerequisite_course in prerequisite:
            try:
                exists = StudentCourse.objects.filter(
                student = student,
                semester_course__course = prerequisite_course.prerequisite,
                score__gte = 10 ,
                status = 'R'
                ).exists()
            except Exception as e:
                pass
            if not exists:
                raise serializers.ValidationError("prerequisite not met!")
        

        #requisite
        try:
            requisite = Requisite.objects.filter(course = basic_course)
        except Exception as e:
            pass
        for requisite_course in requisite:
            try:
                exists = StudentCourse.objects.filter(student = student,
                                                    semester_course__course = requisite_course.requisite ,
                                                    semester_course__semester = semester ,
                                                    status = 'R' ,
                                                    ).exists()
                
            except Exception as e:
                pass
            if not exists:
                raise serializers.ValidationError("requisite not met!")

        
        

        
        with transaction.atomic():
            # Create the UnitSelectionRequest instance
            unit_selection_request = UnitSelectionRequest.objects.create(
            semester_registration_request=semester_registration_request,
            approval_status='P',
            request_course=request_course
                )
            
            # Add to Student Courses
            StudentCourse.objects.create(
                        student = student ,
                        semester_course = request_course ,
                        status='R',
                        )

        return unit_selection_request

class StudentDeleteSemesterRequestSerializer(serializers.ModelSerializer):
    # semester_registration_request = UnitSelectionSemesterRegistrationRequestSerializer()
    class Meta:
        model = StudentDeleteSemesterRequest
        fields = ['id', 'semester_registration_request', 'teacher_approval_status',
                  'educational_assistant_approval_status', 'created_at',
                  'student_explanations', 'educational_assistant_explanation']

        read_only_fields = ['id', 'semester_registration_request', 'teacher_approval_status',
                            'educational_assistant_approval_status', 'created_at',
                            'educational_assistant_explanation']

    def create(self, validated_data):
        user = self.context['user']
        semester = Semester.objects.order_by('-start_semester').first()
        try:
            semester_registration_request = SemesterRegistrationRequest.objects.get(
                semester = semester ,
                student__user = user
            )
        except Exception as e:
            raise serializers.ValidationError("Invalid SemesterRegistrationRequest")

        existing_request = StudentDeleteSemesterRequest.objects.filter(
            semester_registration_request=semester_registration_request,
            semester_registration_request__student__user=user ,
            ).filter(Q(teacher_approval_status = 'P') | Q(educational_assistant_approval_status = 'P')).exists()
        
        if existing_request:
            raise serializers.ValidationError(
                "A request for this semester already exists")

        current_date = timezone.now().date()

        if (current_date < semester.start_semester or
                current_date > semester.end_semester
        ):
            raise serializers.ValidationError("Unavailable semester")

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
            course = StudentCourse.objects.get(pk=student_course_pk,
                                               student=student)
        except Exception:
            raise serializers.ValidationError("Invalid course")

        if course.status == 'F':
            raise serializers.ValidationError("Final register!")
        
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
        return RevisionRequest.objects.create(
                student=student, course=course, text=validated_data['text'])



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
        
        student_course = validated_data.get('course')
        user = self.context['user']
        try:
            student = Student.objects.get(user=user)
        except:
            raise serializers.ValidationError("Invalid student")

        try:
            course = StudentCourse.objects.get(
                        pk=student_course ,
                        student=student ,
                        status = 'R')
        except Exception:
            raise serializers.ValidationError("Invalid course")
        # try:
        #     current_date = timezone.now().date()
        #     emergency_start = course.semester_course.semester.emergency.emergency_remove_start
        #     emergency_end = course.semester_course.semester.emergency.emergency_remove_end
        # except Exception as e:
        #     raise serializers.ValidationError("semester emergency not set!")
        # if current_date < emergency_start:
        #     raise serializers.ValidationError("Emergency remove not accesible")
        # elif current_date > emergency_end:
        #     raise serializers.ValidationError("Emergency remove ended")

        existing_request = EmergencyRemovalRequest.objects.filter(
            course=course, student=student, approval_status='P').first()

        if existing_request != None:
            raise serializers.ValidationError("A registration request for this course already exists")

        validated_data['course'] = course
        emergency_removal_request = EmergencyRemovalRequest.objects.create(
                student=student,
                course=course,
                student_explanation=validated_data['student_explanation'])

        return emergency_removal_request


class AddRemoveRequestSerializer(serializers.ModelSerializer):
    request_course = SemesterCourseSerializer()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request') and self.context['request'].method == 'POST':
            self.fields['approval_status'].default = 'A'
    class Meta:
        model = UnitSelectionRequest
        fields = ['id', 'semester_registration_request', 'approval_status',
                  'created_at', 'request_course']
        read_only_fields = ['id', 'created_at', 'approval_status']
    def get_fields(self):
        fields = super().get_fields()
        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['request_course'] = serializers.PrimaryKeyRelatedField(
                queryset = SemesterCourse.objects.all()
            )
            # fields['semester_registration_request'] = serializers.PrimaryKeyRelatedField(
            #     queryset = SemesterRegistrationRequest.objects.all()
            # )
            fields.pop('semester_registration_request')
            
        return fields
    def create(self, validated_data):
        user = self.context['user']
        student = Student.objects.get(user=user)
        department = student.major.department
        # print(gpa_catergory(student.gpa))
        # semester_registration_request = validated_data.get('semester_registration_request')
        # if semester_registration_request.student != student:
        #     raise serializers.ValidationError("wrong semester registration request")
        # semester = semester_registration_request.semester

        semester = Semester.objects.order_by('-start_semester').first()
        try:
            semester_registration_request = SemesterRegistrationRequest.objects.get(
                semester = semester ,
                student = student ,
                approval_status = 'A')
        except:
            raise serializers.ValidationError("wrong semester registration request")
        request_course = validated_data.get('request_course')
        
        if request_course.semester != semester:
            raise serializers.ValidationError("invalid course")
        
        try:
            remain_credit = find_remain_credit(student)
        except Exception as e:
            pass
        if remain_credit==0 or request_course.course.credit_num > remain_credit:
            raise serializers.ValidationError("You can not add more courses")

        # check course capacity
        remain_capacity = request_course.remain_course_capacity
        if remain_capacity == 0:
            # Save request to Redis
            save_to_redis(validated_data.get('request_course').id, user.id)
            raise serializers.ValidationError(
                "You cannot add course because the course capacity is full but is reserved for you"
                )
        
        # check for request_course department
        course_department = request_course.course.department

        if course_department != department:
            raise serializers.ValidationError(
                "Invalid requested course, course not in your department!"
            )
        
        basic_course = request_course.course
        # #Prerequisite
        
        try:
            prerequisite = Prerequisite.objects.filter(course = basic_course)
        except Exception as e:
            pass
        for prerequisite_course in prerequisite:
            try:
                exists = StudentCourse.objects.filter(
                student = student,
                semester_course__course = prerequisite_course.prerequisite,
                score__gte = 10 ,
                status = 'R'
                ).exists()
            except Exception as e:
                pass
            if not exists:
                raise serializers.ValidationError("prerequisite not met!")
        

        #requisite
        try:
            requisite = Requisite.objects.filter(course = basic_course)
        except Exception as e:
            pass
        for requisite_course in requisite:
            try:
                exists = StudentCourse.objects.filter(student = student,
                                                    semester_course__course = requisite_course.requisite ,
                                                    semester_course__semester = semester ,
                                                    status = 'R' ,
                                                    ).exists()
                
            except Exception as e:
                pass
            if not exists:
                raise serializers.ValidationError("requisite not met!")

        
        

        
        with transaction.atomic():
            # Create the UnitSelectionRequest instance
            unit_selection_request = UnitSelectionRequest.objects.create(
            semester_registration_request=semester_registration_request,
            approval_status='P',
            request_course=request_course
                )
            
            # Add to Student Courses
            StudentCourse.objects.create(
                        student = student ,
                        semester_course = request_course ,
                        status='R',
                        )

        return unit_selection_request



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
