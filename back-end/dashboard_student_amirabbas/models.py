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
    modified_courses = models.ManyToManyField(SemesterCourse, related_name='modified_courses')
    reason_text = models.TextField(blank=False)

class UniversityAddRemoveRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    added_universities = models.ManyToManyField(Semester, related_name='added_universities')
    removed_universities = models.ManyToManyField(Semester, related_name='removed_universities')

class RevisionRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.TextField()


class EnrollmentRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    reason_text= models.TextField(blank=False)

class RemoveDuplicateRequest(models.Model):
    semester_registration_request = models.ForeignKey(
        SemesterRegistrationRequest, on_delete=models.CASCADE)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    removed_duplicates = models.ManyToManyField(StudentCourse, related_name='removed_duplicates')



class CourseModificationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    modified_courses = models.ManyToManyField(SemesterCourse, related_name='modified_courses')
    reason_text = models.TextField(blank=False)