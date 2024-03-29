from django.db import models
from accounts.models import Student, Teacher
from education.models import SemesterCourse , StudentCourse , Semester



APPROVAL_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]
class SemesterRegistrationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    semester = models.ForeignKey(Semester , on_delete = models.PROTECT)
    

class UnitSelectionRequest(models.Model):
    semester_registration_request = models.OneToOneField(
        SemesterRegistrationRequest , on_delete=models.CASCADE)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    requested_courses = models.ManyToManyField(SemesterCourse, verbose_name='Requested_courses')


class AddRemoveRequest(models.Model):
    semester_registration_request = models.ForeignKey(
        SemesterRegistrationRequest , on_delete=models.CASCADE)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    removed_courses = models.ManyToManyField(StudentCourse, related_name='removed_courses')
    added_courses = models.ManyToManyField(SemesterCourse, related_name='added_courses')


class RevisionRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.TextField()


class EmergencyRemovalRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()


class StudentDeleteSemesterRequest(models.Model):
    semester_registration_request = models.ForeignKey(
        SemesterRegistrationRequest , on_delete=models.CASCADE)
    teacher_approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    educational_assistant_approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    student_explanations = models.TextField()
    educational_assistant_explanation = models.TextField()


class EnrollmentRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    reason_text= models.TextField(blank=False)


class EmploymentEducationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)