from rest_framework import serializers
from education.models import Day, Major, Prerequisite, Requisite, SemesterClass, SemesterCourse , Semester , Department , \
                                Course , StudentCourse
from accounts.models import Student,  User , Teacher
from .models import SemesterRegistrationRequest , RevisionRequest ,  \
                    EnrollmentRequest ,  UniversityAddRemoveRequest
from django.utils import timezone


        
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

class CourseSerializer(serializers.ModelSerializer):
    prerequisites = 'PrerequisiteSerializer()'
    required_by = 'RequisiteSerializer()'
    class Meta:
        model = Course
        fields = ['course_name','course_code','credit_num','prerequisites','required_by']

class SemesterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterClass
        fields = ['classes_start', 'classes_end']


class SemesterSerializer(serializers.ModelSerializer):
    classes = SemesterClassSerializer()
    class Meta:
        model = Semester
        fields = ['name' , 'classes']
        

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
    class_days = ClassDaysSerializer()
    class Meta:
        model = SemesterCourse
        fields = ['semester','course','class_days','class_time_start','class_time_end',
                  'instructor','course_capacity','remain_course_capacity']
        

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    advisor = TeacherSerializer()
    class Meta:
        model = Student
        fields = ['user', 'entry_semester', 'gpa', 'entry_year'
                  , 'advisor', 'military_service_status', 'year_of_study','major']
        


class ExamSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']
class ExamSemesterCourseSerializer(serializers.ModelSerializer):
    semester = ExamSemesterSerializer()
    course = CourseSerializer()
    class Meta:
        model = SemesterCourse

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['major_name','major_code', 'level', 'education_group']


class SemesterRegistrationRequestSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']
class SemesterRegistrationRequestSerializer(serializers.ModelSerializer):
    semester = SemesterRegistrationRequestSemesterSerializer()
    class Meta:
        model = SemesterRegistrationRequest
        fields = ['id','approval_status', 'created_at','semester']
        
        read_only_fields = ['id','approval_status', 'created_at']
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

class UniversityAddRemoveRequestSerializerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['name']

class UniversityAddRemoveRequestSerializer(serializers.ModelSerializer):
    StudentCourse = UniversityAddRemoveRequestSerializerSerializer()
    class Meta:
        model = UniversityAddRemoveRequest
        fields = ['id', 'student', 'approval_status', 'created_at', 'semester', 'added_universities', 'removed_universities']
        read_only_fields = ['id', 'approval_status', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user  # دریافت کاربری که درخواست را ارسال کرده است
        semester = validated_data.get('semester')
        added_universities = validated_data.get('added_universities', [])
        removed_universities = validated_data.get('removed_universities', [])

        try:
            # Check the end date of the semester  

            if semester.end_date < timezone.now().date():
                raise serializers.ValidationError("This semester has ended!")

            # Checking the account settlement before starting to delete and add 

            if semester.start_date < timezone.now().date():
                raise serializers.ValidationError("Financial clearance must be completed before add/remove")
            
            # Checking that deletion and addition are done after selecting the unit   

            if semester.unit_selection_end < timezone.now().date():
                raise serializers.ValidationError("Add/remove must be done after unit selection")

            # Checking the number of units
            
            total_units = sum(course.units for course in added_universities)
            if total_units > 6:
                raise serializers.ValidationError("Maximum 6 units can be added")

            # Check repeated lessons   
               
            course_codes = [course.code for course in added_universities]
            if len(set(course_codes)) != len(course_codes):
                raise serializers.ValidationError("Duplicate courses are not allowed")

            # Create request
          
            request = UniversityAddRemoveRequest.objects.create(student=user, **validated_data)
            return request

        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise serializers.ValidationError("An error occurred while processing your request. Please try again later.")
        




