from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from dashboard_student.models import (
    EmergencyRemovalRequest,
    StudentDeleteSemesterRequest,
    EmploymentEducationRequest
)
from accounts.models import User

class EmergencyRemovalRequestTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_emergency_removal_request(self):
        url = reverse('emergency_removals-list')  # Updated URL name
        data = {
            'student': 1,  # Assuming student ID exists in your database
            # Add other required fields here
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmergencyRemovalRequest.objects.count(), 1)

    # Add more test cases as needed

class StudentDeleteSemesterRequestTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_student_delete_semester_request(self):
        url = reverse('semester_removals-list')  # Updated URL name
        data = {
            'semester_registration_request': 1,  # Assuming semester registration request ID exists in your database
            # Add other required fields here
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudentDeleteSemesterRequest.objects.count(), 1)

    # Add more test cases as needed

class EmploymentEducationRequestTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_employment_education_request(self):
        url = reverse('education_employments-list')  # Updated URL name
        data = {
            'student': 1,  # Assuming student ID exists in your database
            # Add other required fields here
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmploymentEducationRequest.objects.count(), 1)

    # Add more test cases as needed
