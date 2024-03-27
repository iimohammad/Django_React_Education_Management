from rest_framework import serializers
from education.models import SemesterCourse , Semester , Department , Course , StudentCourse , Major
from accounts.models import Student, Teacher , User
from .models import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name', 'department_code', 'year_established', 
                  'department_location']
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name' ,'last_name','email' , 'user_number', 
                  'national_code', 'birthday', 'profile_image', 'phone', 'address', 'gender']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    department = DepartmentSerializer()
    class Meta:
        model = Teacher
        fields = ['user', 'expertise', 'rank', 'department']

class MajorSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()

    class Meta:
        model = Major
        fields = ['major_name', 'major_code', 'department', 'number_of_credits', 'level', 'education_group']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name','start_semester','end_semester','semester_type',]
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        prerequisite = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())
        corequisite = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())
        fields = ['course_name','course_code','credit_num','prerequisite','corequisite']
class SemesterCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterCourse
        semester = SemesterSerializer
        instructor = TeacherSerializer
        course = CourseSerializer
        fields = ['semester','course','class_days','class_time','exam_datetime',
                  'exam_location','instructor','course_capacity']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name' ,'last_name','email' , 'user_number', 
                  'national_code', 'birthday', 'profile_image', 'phone', 'address', 'gender']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Student
        fields = ['user', 'entry_semester', 'gpa', 'entry_year'
                  , 'advisor', 'military_service_status', 'year_of_study','major']
        
class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        student = StudentSerializer
        semester_course = SemesterCourseSerializer
        fields = ['student','semester_course','status','score']

