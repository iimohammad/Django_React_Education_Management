from rest_framework import serializers
from education.models import SemesterClass, SemesterCourse , Semester , Department , \
                                Course , StudentCourse
from accounts.models import Student, Teacher , User
from .models import SemesterRegistrationRequest , RevisionRequest , AddRemoveRequest , \
                    EnrollmentRequest , EmergencyRemovalRequest , StudentDeleteSemesterRequest , \
                    EmploymentEducationRequest
from django.utils import timezone


# class EnrollmentRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EnrollmentRequest
#         fields = '__all__'

# class EducationalAssistantEnrollmentRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EnrollmentRequest
#         fields = '__all__'

# class StudentEnrollmentRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EnrollmentRequest
#         exclude = ['is_approved']
        
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name', 'department_code', 'year_established', 
                  'department_location']
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name' ,'last_name','profile_image']

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
        fields = ['name' , 'classes']
class CourseSerializer(serializers.ModelSerializer):
    prerequisite = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())
    corequisite = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())
    class Meta:
        model = Course
        fields = ['course_name','course_code','credit_num','prerequisite','corequisite']
class SemesterCourseSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    course = CourseSerializer()
    instructor = TeacherSerializer()
    class Meta:
        model = SemesterCourse
        fields = ['semester','course','class_days','class_time',
                  'instructor','course_capacity','remain_course_capacity']
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    advisor = TeacherSerializer()
    class Meta:
        model = Student
        fields = ['user', 'entry_semester', 'gpa', 'entry_year'
                  , 'advisor', 'military_service_status', 'year_of_study','major']
class StudentCourseSerializer(serializers.ModelSerializer):
    semester_course = SemesterCourseSerializer()
    class Meta:
        model = StudentCourse
        fields = ['semester_course','status','score']

class ExamSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']
class ExamSemesterCourseSerializer(serializers.ModelSerializer):
    semester = ExamSemesterSerializer()
    course = CourseSerializer()
    class Meta:
        model = SemesterCourse
        fields = ['semester','course','exam_datetime' , 'exam_location']

class ExamStudentCourseSerializer(serializers.ModelSerializer):
    semester_course = ExamSemesterCourseSerializer()
    class Meta:
        model = StudentCourse
        fields = ['semester_course']


class ProfileStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    advisor = TeacherSerializer()
    class Meta:
        model = Student
        fields = ['user','entry_semester', 'gpa', 'entry_year'
                  , 'advisor', 'military_service_status', 'year_of_study','major']


class SemesterRegistrationRequestSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']

class SemesterRegistrationRequestSerializer(serializers.ModelSerializer):
    semester = SemesterRegistrationRequestSemesterSerializer()
    class Meta:
        model = SemesterRegistrationRequest
        fields = ['id','status', 'teacher_visited','educational_assistant_visited' ,
                  'created_at' , 'semester','explanation']
        
        read_only_fields = ['status', 'teacher_visited','educational_assistant_visited' ,
                            'created_at' ,'explanation']
    def create(self, validated_data):
        semester_data = validated_data.pop('semester')
        user = self.context['user']
        
        try:
            semester_instance = Semester.objects.get(name=semester_data['name'])
            if semester_instance.classes.classes_end < timezone.now().date():
                raise serializers.ValidationError("This semester ended!")
        except Semester.DoesNotExist:
            raise serializers.ValidationError("Invalid semester")
        
        existing_request = SemesterRegistrationRequest.objects.filter(semester=semester_instance, student__user=user).exists()
        if existing_request:
            raise serializers.ValidationError("A registration request for this semester already exists")
        
        try:
            student = Student.objects.get(user = user)
        except Semester.DoesNotExist:
            raise serializers.ValidationError("Invalid student")
        
        semester_registration_request = SemesterRegistrationRequest.objects.create(semester=semester_instance, student = student)

        return semester_registration_request
    

