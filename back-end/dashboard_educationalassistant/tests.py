import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from dashboard_student.models import RevisionRequest
from accounts.models import Teacher , Student , EducationalAssistant
from education.models import Department , Semester , StudentCourse , \
                            Course , SemesterCourse ,Major
User = get_user_model()


# Create your tests here.
class tests(APITestCase):
    def setUp(self):
        self.semester = Semester.objects.create(
            name = '20241',
            start_semester = '2024-02-01',
            end_semester = '2024-04-01',
            semester_type = 'F'
        )
        self.department = Department.objects.create(
            department_name='computer' , 
            department_code = 1 , 
            year_established = '2000-01-01',
            department_location = 'test'
        )
        self.major = Major.objects.create(
            major_name = 'sofware',
            major_code = 1 ,
            department = self.department ,
            number_of_credits = 140 ,
            level = 'B',
            education_group = 'test'
        )
        self.course = Course.objects.create(
            course_name = 'programming1',
            course_code = 10 ,
            department = self.department ,
            major = self.major ,
            credit_num = 3 ,
            course_type = 'G',
            availablity = 'A'
        )
        self.teacher_user = User.objects.create(
            username='teacher', 
            password='teacherpassword',
            user_number = '123456',
            national_code = '1234567890',
            phone = '09111111111',
            gender = 'M' ,
            email = 'abcd@abc.com'
            )
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            expertise = 'asd',
            rank = 'I',
            department = self.department,
            can_be_advisor = True)
        self.student_user = User.objects.create(
            username='student', 
            password='studentpassword',
            user_number = '123456',
            national_code = '1234567890',
            phone = '09111111111',
            gender = 'M' ,
            email = 'abc@abc.com'
            )
        self.student = Student.objects.create(
            user = self.student_user ,
            entry_semester = '20201',
            entry_year = '2020',
            major = self.major ,
            advisor = self.teacher ,
            military_service_status = 'EP',
            year_of_study = 2
        )
        self.education_user = User.objects.create(
            username='education', 
            password='educationpassword',
            user_number = '123455',
            national_code = '1234567810',
            phone = '09111111111',
            gender = 'M' ,
            email = 'babc@abc.com'
            )
        self.education = EducationalAssistant.objects.create(
            user = self.education_user ,
            field = self.major ,
            )
        self.semester_course = SemesterCourse.objects.create(
            semester = self.semester ,
            course = self.course ,
            class_time_start = '10:00:00',
            class_time_end = '12:00:00',
            instructor = self.teacher , 
            course_capacity = 30
        )
        self.student_course = StudentCourse.objects.create(
            student = self.student,
            semester_course = self.semester_course ,
            status = 'R' ,
            score = 10
        )
        self.revision_request = RevisionRequest.objects.create(
            student = self.student ,
            course = self.student_course ,
            text = 'text'
        )
    def test_retrieve_students_list(self):
        url = '/dashboard_educationalassistant/students/'
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_students_list_no_permision(self):
        url = '/dashboard_educationalassistant/students/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_retrieve_teachers_list(self):
        url = '/dashboard_educationalassistant/teachers/'
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_teachers_list_no_permision(self):
        url = '/dashboard_educationalassistant/teachers/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_retrieve_education_profile(self):
        url = reverse('show_assistant_profile')
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_education_profile(self):
        url = reverse('edit_assistant_profile')
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_education_profile_change(self):
        data ={
            "username":'education', 
            'password':'educationpassword',
            'user_number' : '123455',
            'national_code' : '1234567810',
            'phone' : '09111111111',
            'gender' : 'M' ,
            'email' : 'cac@abc.com'
        }
        url = reverse('edit_assistant_profile')
        self.client.force_authenticate(user=self.education_user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_students_passed_courses_list(self):
        url = '/dashboard_educationalassistant/students_passed_courses/'
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_students_registred_courses_list(self):
        url = reverse('students_registered_courses-list')
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_retrieve_students_courses_list(self):
        url = '/dashboard_educationalassistant/courses/'
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_course_object(self):
        url = f'/dashboard_educationalassistant/courses/{self.course.id}/'
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_retrieve_semester_courses_list(self):
        url = '/dashboard_educationalassistant/semester_courses/'
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_semester_courses_object(self):
        url = f'/dashboard_educationalassistant/semester_courses/{self.semester_course.id}/'
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_retrieve_emergency_remove_list(self):
        url = reverse('emergency_removals-list')
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_semester_remove_list(self):
        url = reverse('semester_removals-list')
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_education_employments_list(self):
        url = reverse('education_employments-list')
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_revision_requests_list(self):
        url = reverse('revision_requests-list')
        self.client.force_authenticate(user=self.education_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

