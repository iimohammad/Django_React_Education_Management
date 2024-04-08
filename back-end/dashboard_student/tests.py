from django.test import TestCase
from django.contrib.auth.models import User
from django.db import models
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import Student, Teacher
from education.models import SemesterCourse , StudentCourse , Semester
from .serializers import SemesterCourseSerializer, StudentCourseSerializer, ExamSemesterSerializer, ExamSemesterCourseSerializer, ExamStudentCourseSerializer , ProfileStudentSerializer,SemesterRegistrationRequestSerializer , StudentDeleteSemesterRequest
from .models import SemesterCourse, SemesterRegistrationRequest, UnitSelectionRequest

class SemesterCourseAPITest(APITestCase):
    def setUp(self):
        self.semester = Semester.objects.create(name='Spring 2024')
        self.semester_course_1 = SemesterCourse.objects.create(
            semester=self.semester,  
            course_name='Course 1',   
            class_days=1,    
            class_time_start='09:00:00',
            class_time_end='11:00:00',
            instructor=1,   
            course_capacity=30,
            remain_course_capacity=30
        )
        self.semester_course_2 = SemesterCourse.objects.create(
            semester=self.semester,  
            course_name='Course 2',    
            class_days=2,   
            class_time_start='10:00:00',
            class_time_end='12:00:00',
            instructor=2,  
            course_capacity=25,
            remain_course_capacity=25
        )

    def test_get_semester_courses(self):
        url = reverse('semester_courses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = SemesterCourseSerializer([self.semester_course_1, self.semester_course_2], many=True).data
        self.assertEqual(response.data, expected_data) 
    
    def test_create_semester_course(self):
        url = reverse('semester_courses')
        data = {
            'semester': self.semester.id,  
            'course_name': 'Course 3',  
            'class_days': 1,    
            'class_time_start': '09:00:00',
            'class_time_end': '11:00:00',
            'instructor': 1,    
            'course_capacity': 30,
            'remain_course_capacity': 30
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SemesterCourse.objects.filter(semester=data['semester'], course_name=data['course_name']).exists())


    def test_update_semester_course(self):
        url = reverse('semestercourse-detail', kwargs={'pk': self.semester_course_1.pk})
        data = {
            'course_capacity': 40
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the course is updated in the database
        self.semester_course_1.refresh_from_db()
        self.assertEqual(self.semester_course_1.course_capacity, 40)

    def test_delete_semester_course(self):
        url = reverse('semestercourse-detail', kwargs={'pk': self.semester_course_1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the course is deleted from the database
        self.assertFalse(SemesterCourse.objects.filter(pk=self.semester_course_1.pk).exists())

    
class StudentCourseAPITestCase(APITestCase):

    def setUp(self):
        # Create users
        self.student_user = User.objects.create(username='student_test', email='student@test.com')
        self.student = Student.objects.create(user=self.student_user)
        self.teacher_user = User.objects.create(username='teacher_test', email='teacher@test.com')
        self.teacher = Teacher.objects.create(user=self.teacher_user)

        # Create a semester
        self.semester = Semester.objects.create(name='Spring 2024')

        # Create a semester course
        self.semester_course = SemesterCourse.objects.create(semester=self.semester, course_name='Advanced Algorithms')

    def test_create_student_course(self):
        url = reverse('student_courses')
        data = {
            'student': self.student.id,
            'semester_course': self.semester_course.id,
            'status': 'Enrolled',
            'score': 90
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudentCourse.objects.count(), 1)
        self.assertEqual(StudentCourse.objects.get().status, 'Enrolled')

    def test_get_student_course(self):
        student_course = StudentCourse.objects.create(student=self.student, semester_course=self.semester_course, status='Enrolled', score=90)
        url = reverse('student_courses', kwargs={'pk': student_course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Enrolled')

    def test_update_student_course(self):
        student_course = StudentCourse.objects.create(student=self.student, semester_course=self.semester_course, status='Enrolled', score=90)
        url = reverse('student_courses', kwargs={'pk': student_course.id})
        data = {'status': 'Completed', 'score': 95}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(StudentCourse.objects.get(pk=student_course.id).status, 'Completed')
        self.assertEqual(StudentCourse.objects.get(pk=student_course.id).score, 95)

    def test_delete_student_course(self):
        student_course = StudentCourse.objects.create(student=self.student, semester_course=self.semester_course, status='Enrolled', score=90)
        url = reverse('student_courses', kwargs={'pk': student_course.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(StudentCourse.objects.count(), 0)


class StudentPassedCoursesViewSetTest(APITestCase):
    def setUp(self):
   
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.student = Student.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_passed_courses(self):
        semester = Semester.objects.create(name='Spring 2024')
        semester_course = SemesterCourse.objects.create(
            course_name='Test Course',
            semester=semester
        )
        StudentCourse.objects.create(
            student=self.student,
            semester_course=semester_course,
            score=80 
        )

        url = reverse('passed_courses') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

    def test_create_passed_course(self):
        semester = Semester.objects.create(name='Spring 2024')
        semester_course = SemesterCourse.objects.create(
            course_name='Test Course',
            semester=semester
        )

        data = {
            'student': self.student.id,
            'semester_course': semester_course.id,
            'score': 90  
        }

        url = reverse('passed_courses')  
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_passed_course(self):
        semester = Semester.objects.create(name='Spring 2024')
        semester_course = SemesterCourse.objects.create(
            course_name='Test Course',
            semester=semester
        )
        student_course = StudentCourse.objects.create(
            student=self.student,
            semester_course=semester_course,
            score=80  
        )

        data = {
            'score': 85  
        }

        url = reverse('passed_courses', kwargs={'pk': student_course.id})  
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class StudentExamsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.student = Student.objects.create(user=self.user)
        self.client.login(username='test_user', password='test_password')

    def test_get_student_exams(self):
        url = reverse('student_exams')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_exam(self):
        semester = Semester.objects.create(name='Test Semester')
        semester_course = SemesterCourse.objects.create(semester=semester)
        data = {'semester_course': semester_course.id}
        url = reverse('student_exams')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_student_exam(self):
        semester = Semester.objects.create(name='Test Semester')
        semester_course = SemesterCourse.objects.create(semester=semester)
        student_course = StudentCourse.objects.create(student=self.student, semester_course=semester_course)
        student_exam = StudentCourse.objects.create(student=self.student, semester_course=semester_course)
        new_semester_course = SemesterCourse.objects.create(semester=semester)
        data = {'semester_course': new_semester_course.id}
        url = reverse('student_exams', kwargs={'pk': student_exam.id})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class StudentProfileViewsetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword')
        self.student = Student.objects.create(
            user=self.user, entry_semester='Spring', gpa=3.5, entry_year=2022)
        self.client.force_login(self.user)

    def test_get_student_profile(self):
        url = reverse('profile/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ProfileStudentSerializer(instance=self.student)
        self.assertEqual(response.data, serializer.data)

class SemesterRegistrationRequestAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.student = Student.objects.create(user=self.user)
        self.semester = Semester.objects.create(name='Test Semester')
        self.course1 = SemesterCourse.objects.create(name='Course 1', semester=self.semester)
        self.course2 = SemesterCourse.objects.create(name='Course 2', semester=self.semester)

    def test_create_semester_registration_request(self):
        url = reverse('semester-registration-request-list')  # Replace 'semester-registration-request-list' with your actual URL name
        data = {
            'student': self.student.id,
            'semester': self.semester.id,
            'requested_courses': [self.course1.id, self.course2.id]
        }
        self.client.force_login(self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SemesterRegistrationRequest.objects.count(), 1)

    def test_retrieve_semester_registration_request(self):
        semester_registration_request = SemesterRegistrationRequest.objects.create(
            student=self.student,
            semester=self.semester
        )
        url = reverse('semester_registration', kwargs={'pk': semester_registration_request.id})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = SemesterRegistrationRequestSerializer(instance=semester_registration_request)
        self.assertEqual(response.data, serializer.data)

    def test_update_semester_registration_request(self):
        semester_registration_request = SemesterRegistrationRequest.objects.create(
            student=self.student,
            semester=self.semester
        )
        url = reverse('semester_registration', kwargs={'pk': semester_registration_request.id})
        updated_data = {
            'approval_status': 'A' 
        }
        self.client.force_login(self.user)
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        semester_registration_request.refresh_from_db()
        self.assertEqual(semester_registration_request.approval_status, 'A')


class UnitSelectionRequestAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.student = Student.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.semester = Semester.objects.create(name='Test Semester')
        self.course1 = SemesterCourse.objects.create(name='Course 1', semester=self.semester)
        self.course2 = SemesterCourse.objects.create(name='Course 2', semester=self.semester)
        self.registration_request = SemesterRegistrationRequest.objects.create(
             student=self.student, semester=self.semester
        )

    def test_create_unit_selection_request(self):
        url = reverse('unit_selection')
        data = {
            'semester_registration_request': self.registration_request.id,
            'requested_courses': [self.course1.id, self.course2.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_unit_selection_request(self):
        unit_selection_request = UnitSelectionRequest.objects.create(
            semester_registration_request=self.registration_request
        )
        url = reverse('unit_selection', args=[unit_selection_request.id])
        data = {'approval_status': 'A'} 
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['approval_status'], 'A')

 
class StudentDeleteSemesterRequestAPITest(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(username='student', password='password')
        self.student = Student.objects.create(user=self.student_user)
        self.client.force_authenticate(user=self.student_user)
        self.semester = Semester.objects.create(name='Test Semester')
        self.semester_registration_request = SemesterRegistrationRequest.objects.create(
            student=self.student, semester=self.semester)

    def test_create_student_delete_semester_request(self):
        url = reverse('delete_semester_request')

        data = {
            'semester_registration_request': self.semester_registration_request.id,
            'student_explanations': 'Test explanation'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_student_delete_semester_request(self):
        # Create a student delete semester request
        student_delete_semester_request = StudentDeleteSemesterRequest.objects.create(
            semester_registration_request=self.semester_registration_request,
            student_explanations='Initial explanation'
        )

        url = reverse('delete_semester_request', kwargs={'pk': student_delete_semester_request.id})

        updated_explanation = 'Updated explanation'
        data = {
            'student_explanations': updated_explanation
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(StudentDeleteSemesterRequest.objects.get(id=student_delete_semester_request.id).student_explanations, updated_explanation)

    def test_get_student_delete_semester_request(self):
        student_delete_semester_request = StudentDeleteSemesterRequest.objects.create(
            semester_registration_request=self.semester_registration_request,
            student_explanations='Test explanation'
        )

        url = reverse('delete_semester_request', kwargs={'pk': student_delete_semester_request.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

