from rest_framework import serializers

from accounts.models import Student, Teacher, User, EducationalAssistant
from education.models import Department, Major, StudentCourse


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
        fields = ['department_name', 'department_code', 'year_established',
                  'department_location']


class MajorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Major
        fields = ['major_name', 'major_code', 'department',
                  'number_of_credits', 'level', 'education_group']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    major = MajorSerializer()

    class Meta:
        model = Student
        fields = [
            'user',
            'entry_semester',
            'gpa',
            'entry_year',
            'major',
            'advisor',
            'military_service_status',
            'year_of_study',
            'major']


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
        fields = ['user', 'field']


class StudentCoursePassSerializer(serializers.ModelSerializer):
    semester_course = serializers.SerializerMethodField()

    class Meta:
        model = StudentCourse
        fields = ['semester_course']

    def get_semester_course(self, obj):
        if obj.status == 'R' and obj.score != '':
            return obj.semester_course
        else:
            return None


class StudentCourseTermSerializer(serializers.ModelSerializer):
    semester_course = serializers.SerializerMethodField()

    class Meta:
        model = StudentCourse
        fields = ['semester_course']

    def get_semester_course(self, obj):
        if obj.status == 'R' and obj.score == '':
            return obj.semester_course
        else:
            return None



    
    
    