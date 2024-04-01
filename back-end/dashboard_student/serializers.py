from rest_framework import serializers
from education.models import Day, Major, Prerequisite, Requisite, SemesterClass, SemesterCourse , Semester , Department , \
                                Course , StudentCourse
from accounts.models import Student, Teacher , User
from .models import SemesterRegistrationRequest , RevisionRequest , AddRemoveRequest , \
                    EnrollmentRequest , EmergencyRemovalRequest , StudentDeleteSemesterRequest , \
                    EmploymentEducationRequest, UnitSelectionRequest
from django.utils import timezone
from rest_framework.exceptions import NotFound


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
    prerequisites = 'PrerequisiteSerializer()'
    required_by = 'RequisiteSerializer()'
    class Meta:
        model = Course
        fields = ['course_name','course_code','credit_num','prerequisites','required_by']

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

class MajorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = Major
        fields = ['major_name','major_code', 'level', 'education_group' , 'department']

class ProfileStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    advisor = TeacherSerializer()
    major = MajorSerializer()
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

class UnitSelectionSemesterRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterRegistrationRequest
        fields = ['id']

class UnitSelectionRequestSerializer(serializers.ModelSerializer):
    semester_registration_request = UnitSelectionSemesterRegistrationRequestSerializer()
    requested_courses = SemesterCourseSerializer(many = True)
    class Meta:
        model = UnitSelectionRequest
        fields = ['id','semester_registration_request', 'approval_status',
                    'created_at' , 'requested_courses']
        
        read_only_fields = ['id', 'approval_status','created_at']
    def get_fields(self):
        fields = super().get_fields()

        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['requested_courses'] = serializers.PrimaryKeyRelatedField(queryset=SemesterCourse.objects.all(), many=True)
            fields['semester_registration_request'] = serializers.PrimaryKeyRelatedField(
                queryset=SemesterRegistrationRequest.objects.all())
        
        return fields
    def create(self, validated_data):
        semester_registration_request = validated_data.pop('semester_registration_request')
        user = self.context['user']
        semester= None 
        try:
            semester_registration_request = SemesterRegistrationRequest.objects.get(
                pk=semester_registration_request.pk , 
                student__user = user)
        except SemesterRegistrationRequest.DoesNotExist:
            raise serializers.ValidationError("Invalid SemesterRegistrationRequest")
        
        existing_request = UnitSelectionRequest.objects.filter(
            semester_registration_request=semester_registration_request, 
            semester_registration_request__student__user=user).exists()
        if existing_request:
            raise serializers.ValidationError("A unitselection request for this semester already exists")
        
        try:
            student = Student.objects.get(user = user)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Invalid student")
        
        
        semester = SemesterRegistrationRequest.objects.get(
            pk = semester_registration_request.pk).semester
        current_date = timezone.now().date()
        
        if current_date < semester.unit_selection.unit_selection_start or \
            current_date > semester.unit_selection.unit_selection_end:
                raise serializers.ValidationError("Unvalide semester unit selection time")
        no_capacity = list()
        wrong_semester = list()
        courses = validated_data.pop('requested_courses')
        for i in courses:
            if i.semester != semester:
                wrong_semester.append(i)
            if i.remain_course_capacity==0:
                no_capacity.append(i)
        
        
        if len(wrong_semester)==0 and len(no_capacity)==0:
            unit_selection_request = UnitSelectionRequest.objects.create(
                semester_registration_request = semester_registration_request)
            unit_selection_request.requested_courses.set(courses)
            return unit_selection_request
        else:
            message_wrong_semester = None
            message_no_capacity = None
            if len(wrong_semester)!=0:
                message_wrong_semester = f"this courses belong to another semester: \
                {SemesterCourseSerializer(courses,many = True).data}"
            if len(no_capacity)!=0:
                message_no_capacity = f"this courses have no capacity: \
                    {SemesterCourseSerializer(courses,many = True).data}"
            
            raise serializers.ValidationError(message_wrong_semester+message_no_capacity)
        
class StudentDeleteSemesterRequestSerializer(serializers.ModelSerializer):
    semester_registration_request = UnitSelectionSemesterRegistrationRequestSerializer()
    class Meta:
        model = StudentDeleteSemesterRequest
        fields = ['id','semester_registration_request', 'teacher_approval_status',
                    'educational_assistant_approval_status' , 'created_at',
                    'student_explanations','educational_assistant_explanation']
        
        read_only_fields = ['id','semester_registration_request', 'teacher_approval_status',
                            'educational_assistant_approval_status' , 'created_at',
                            'educational_assistant_explanation']
        

    
    def get_fields(self):
        fields = super().get_fields()

        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['semester_registration_request'] = serializers.PrimaryKeyRelatedField(
                queryset=StudentDeleteSemesterRequest.objects.all())
        return fields
    def create(self, validated_data):
        semester_registration_request = validated_data.pop('semester_registration_request')
        user = self.context['user']
        semester= None
        try:
            semester_registration_request = StudentDeleteSemesterRequest.objects.get(
                pk=semester_registration_request.pk, 
                student__user = user)
        except StudentDeleteSemesterRequest.DoesNotExist:
            raise serializers.ValidationError("Invalid SemesterRegistrationRequest")
        
        existing_request = StudentDeleteSemesterRequest.objects.filter(
            semester_registration_request=semester_registration_request, 
            semester_registration_request__student__user=user).exists()
        if existing_request:
            raise serializers.ValidationError("A unitselection request for this semester already exists")
        
        try:
            student = Student.objects.get(user = user)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Invalid student")
        
        
        semester = StudentDeleteSemesterRequest.objects.get(
            pk = semester_registration_request.pk).semester
        current_date = timezone.now().date()
        
        if current_date < semester.start_semester or \
            current_date > semester.end_semester:
                raise serializers.ValidationError("Unvalide semester")
        
        student_delete_semester_request = StudentDeleteSemesterRequest.objects.create(
                semester_registration_request = semester_registration_request,
                student_explanations = validated_data.get('student_explanations')
                )
        return student_delete_semester_request


class RevisionRequestSerializer(serializers.ModelSerializer):
    course = StudentCourseSerializer()
    class Meta:
        model = RevisionRequest
        fields = ['id', 'course' ,'approval_status',
                    'created_at' , 'text', 'answer']
        
        read_only_fields = ['id','course' ,'approval_status',
                    'created_at' , 'answer' ]
    
    def get_fields(self):
        fields = super().get_fields()

        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['course'] = serializers.IntegerField()
            
        return fields
    
    def create(self, validated_data):
        student_course_pk = validated_data.get('course')
        user = self.context['user']
        try:
            student = Student.objects.get(user = user)
        except:
            raise serializers.ValidationError("Invalid student")
        
        try:
            course = StudentCourse.objects.get(pk = student_course_pk , student = student)
        except Exception:
            raise serializers.ValidationError("Invalid course")

        existing_request = RevisionRequest.objects.filter(
                course=course, student=student ,approval_status = 'P').first()
        
        if existing_request!=None:
            raise serializers.ValidationError("A registration request for this semester already exists")

        
        validated_data['course'] = course
        revision_request = RevisionRequest.objects.create(
            student = student , course = course , text = validated_data['text'])
        
        return revision_request
    
class EmergencyRemovalRequestSerializer(serializers.ModelSerializer):
    course = StudentCourseSerializer()
    class Meta:
        model = EmergencyRemovalRequest
        fields = ['id', 'course' ,'approval_status','created_at' , 
                    'student_explanation','educational_assistant_explanation']
        
        read_only_fields = ['id','approval_status','created_at' , 
                            'educational_assistant_explanation']
    def get_fields(self):
        fields = super().get_fields()

        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['course'] = serializers.IntegerField()
            
        return fields
    
    def create(self, validated_data):
        student_course_pk = validated_data.get('course')
        user = self.context['user']
        try:
            student = Student.objects.get(user = user)
        except:
            raise serializers.ValidationError("Invalid student")
        
        try:
            course = StudentCourse.objects.get(pk = student_course_pk , student = student)
        except Exception:
            raise serializers.ValidationError("Invalid course")

        current_date = timezone.now().date()
        emergency_start = course.semester_course.semester.emergency.emergency_remove_start
        emergency_end = course.semester_course.semester.emergency.emergency_remove_end
        
        if current_date<emergency_start:
            raise serializers.ValidationError("Emergency remove not accesible")
        elif current_date>emergency_end:
            raise serializers.ValidationError("Emergency remove ended")
        
        existing_request = EmergencyRemovalRequest.objects.filter(
                course=course, student=student ,approval_status = 'P').first()
        
        if existing_request!=None:
            raise serializers.ValidationError("A registration request for this semester already exists")

        
        validated_data['course'] = course
        emergency_removal_request = EmergencyRemovalRequest.objects.create(
            student = student , course = course , 
            student_explanation = validated_data['student_explanation'])
        
        return emergency_removal_request