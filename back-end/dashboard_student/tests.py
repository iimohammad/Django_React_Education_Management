from django.test import TestCase
from django.contrib.auth.models import User
from django.db import models
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import Student, Teacher
from education.models import SemesterCourse , StudentCourse , Semester
from .serializers import SemesterCourseSerializer, StudentCourseSerializer, ExamSemesterSerializer, ExamSemesterCourseSerializer, ExamStudentCourseSerializer
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
