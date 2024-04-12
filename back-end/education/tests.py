from django.test import TestCase
from .models import Department, Major, Course, Prerequisite, Requisite, Semester, SemesterUnitSelection, SemesterClass, SemesterAddRemove, SemesterExam, SemesterEmergency, Day, SemesterCourse, StudentCourse
from django.utils import timezone
from accounts.models import Teacher, User,Student


class ModelTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            department_name="Test Department",
            department_code=101,
            year_established=timezone.now(),
            department_location="Test Location"
        )
        self.major = Major.objects.create(
            major_name="Test Major",
            major_code=201,
            department=self.department,
            number_of_credits=120,
            education_group="Test Group"
        )
        self.course = Course.objects.create(
            course_name="Test Course",
            course_code=301,
            department=self.department,
            major=self.major,
            credit_num=3,
            course_type="G",
            availablity="A"
        )

    def test_department_creation(self):
        department = Department.objects.get(department_name="Test Department")
        self.assertEqual(department.department_name, "Test Department")

    def test_major_creation(self):
        major = Major.objects.get(major_name="Test Major")
        self.assertEqual(major.major_name, "Test Major")

    def test_create_semester(self):
        semester = Semester.objects.create(
            name="Test Semester",
            start_semester=timezone.now(),
            end_semester=timezone.now(),
            semester_type="F"
        )
        self.assertEqual(semester.name, "Test Semester")

def test_register_student_for_course(self):
    user = User.objects.create(username="testuser")
    advisor = Teacher.objects.create(name="Test Advisor")  
    student = Student.objects.create(
        user=user,
        entry_semester="Fall",  
        entry_year=timezone.now().year,  
        major=self.major,  
        advisor=advisor, 
        year_of_study=1  
    )
    semester = Semester.objects.create(
        name="Test Semester",
        start_semester=timezone.now(),
        end_semester=timezone.now(),
        semester_type="F"
    )
    semester_course = SemesterCourse.objects.create(
        semester=semester,
        course=self.course,
        class_time_start=timezone.now(),
        class_time_end=timezone.now(),
        instructor=None,
        course_capacity=30
    )
    student_course = StudentCourse.objects.create(
        student=student,
        semester_course=semester_course,
        status="R"
    )
    self.assertEqual(student_course.student, student)

def test_add_prerequisite_for_course(self):
        prerequisite_course = Course.objects.create(
            course_name="Prerequisite Course",
            course_code=401,
            department=self.department,
            major=self.major,
            credit_num=3,
            course_type="G",
            availablity="A"
        )
        prerequisite = Prerequisite.objects.create(
            course=self.course,
            prerequisite=prerequisite_course
        )
        self.assertEqual(prerequisite.course, self.course)

def tearDown(self):
    Department.objects.all().delete()
    Major.objects.all().delete()
    Course.objects.all().delete()
    Prerequisite.objects.all().delete()
    Requisite.objects.all().delete()
    Semester.objects.all().delete()
    SemesterUnitSelection.objects.all().delete()
    SemesterClass.objects.all().delete()
    SemesterAddRemove.objects.all().delete()
    SemesterExam.objects.all().delete()
    SemesterEmergency.objects.all().delete()
    Day.objects.all().delete()
    SemesterCourse.objects.all().delete()
    StudentCourse.objects.all().delete()

