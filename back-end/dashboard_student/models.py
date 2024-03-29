from django.db import models
from accounts.models import Student, Teacher
from education.models import SemesterCourse , StudentCourse , Semester
from education.models import Semester




class SemesterRegistrationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)
    teacher_visited = models.BooleanField(default=False)
    educational_assistant_visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    semester = models.ForeignKey(Semester , on_delete = models.PROTECT)
    explanation = models.TextField(null = True , blank = True)
    

class UnitSelectionRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)
    teacher_visited = models.BooleanField(default=False)
    educational_assistant_visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    semester = models.ForeignKey(Semester , on_delete = models.PROTECT)
    requested_courses = models.ManyToManyField(SemesterCourse, verbose_name='Requested_courses')


class AddRemoveRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)
    teacher_visited = models.BooleanField(default=False)
    educational_assistant_visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    semester = models.ForeignKey(Semester , on_delete = models.PROTECT)
    removed_courses = models.ManyToManyField(StudentCourse, related_name='removed_courses')
    added_courses = models.ManyToManyField(SemesterCourse, related_name='added_courses')


class RevisionRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)
    teacher_visited = models.BooleanField(default=False)
    educational_assistant_visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.TextField()


class EmergencyRemovalRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)
    teacher_visited = models.BooleanField(default=False)
    educational_assistant_visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()


class StudentDeleteSemesterRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)
    teacher_visited = models.BooleanField(default=False)
    educational_assistant_visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    semester = models.ForeignKey(SemesterCourse, on_delete=models.PROTECT)
    student_explanations = models.TextField()
    result = models.CharField(max_length=100)
    educational_assistant_explanation = models.TextField()


class EnrollmentRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)
    teacher_visited = models.BooleanField(default=False)
    educational_assistant_visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    APPROVAL_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    reason_text= models.TextField(blank=False)


class EmploymentEducationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)
    teacher_visited = models.BooleanField(default=False)
    educational_assistant_visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    semester = models.ForeignKey(Semester ,on_delete = models.PROTECT)