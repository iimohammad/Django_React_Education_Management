from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.models import Student, Teacher
from education.models import Department, Major

User = get_user_model()
class SemesterRegistrationRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testteacher', password='testpassword')
        self.department = Department.objects.create(department_name='Test Department', department_code=1, year_established='2022-01-01', department_location='Test Location')
        self.major = Major.objects.create(
            major_name='Computer Science',
            major_code=1,
            department=self.department,
            number_of_credits=120,
            education_group='Science'
        )
    def test_student_creation_with_advisor(self):
        self.teacher = Teacher.objects.create(
            user=self.user,
            expertise='Test Expertise',
            rank=Teacher.Rank.INSTRUCTOR,
            department=self.department,
            can_be_advisor=True
        )
        self.student = Student.objects.create(
            user=self.user,
            entry_semester='Spring',
            entry_year=2022,
            advisor=self.teacher, 
            year_of_study=1,
            major=self.major
        )
        saved_student = Student.objects.get(user=self.user)
        self.assertEqual(saved_student.entry_semester, 'Spring')
        self.assertEqual(int(saved_student.entry_year), 2022)  
        self.assertEqual(saved_student.advisor, self.teacher)
        self.assertEqual(saved_student.year_of_study, 1)
