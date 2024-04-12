import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from dashboard_student.models import RevisionRequest
from accounts.models import Teacher , Student
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
    def test_retrieve_teacher_profile(self):
        url = '/dashboard_professors/show-profile/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_profile_not_teacher(self):
        non_teacher_user = User.objects.create(username='non_teacher', password='non_teacher_password')
        url = '/show-profile/'
        self.client.force_authenticate(user=non_teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_semester_show_get(self):
        self.teacher.can_be_advisor = True
        self.teacher.save()
        url = '/dashboard_professors/TeacherRole/Semester-Show/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_semester_courses_get_list(self):
        self.teacher.can_be_advisor = True
        self.teacher.save()
        url = '/dashboard_professors/TeacherRole/my-Courses-Semester/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_semester_courses_get_course(self):
        self.teacher.can_be_advisor = True
        self.teacher.save()
        url = f'/dashboard_professors/TeacherRole/my-Courses-Semester/{self.student_course.id}/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_revision_request_get_list(self):
        url = '/dashboard_professors/revision-requests/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_revision_request_get_object(self):
        url = f'/dashboard_professors/revision-requests/{self.revision_request.id}/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_revision_request_patch_object(self):
        url = f'/dashboard_professors/revision-requests/{self.revision_request.id}/'
        self.client.force_authenticate(user=self.teacher_user)
        data = {
        'teacher_approval_status': 'A',
        'answer': 'test' ,
        'score' : '19.10'
    }
        response = self.client.patch(url, json.dumps(data),
                                content_type='application/json',
                                HTTP_ACCEPT='application/json; version=v1')
        print('____________')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_show_my_students_get_list(self):
        url = '/dashboard_professors/AdvisorRole/ShowMyStudents/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_show_semester_registration_request_list(self):
        url = '/dashboard_professors/AdvisorRole/SemesterRegistrationConfirmation/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_unit_selection_request_list(self):
        url = '/dashboard_professors/AdvisorRole/UnitSelectionConfirmation/'
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(url, {'HTTP_ACCEPT': 'application/json; version=v1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)