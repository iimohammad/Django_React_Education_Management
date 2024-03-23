from django.db import models
from accounts.models import Student, Teacher
from education.models import SemesterCourse

class StudentRegistrationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    code = models.PositiveSmallIntegerField()
    status = models.BooleanField(default=False)

class SemesterRegistrationRequest(StudentRegistrationRequest):
    requested_courses = models.ManyToManyField(SemesterCourse, verbose_name='Requested_courses')
    
class AddRemoveRequest(StudentRegistrationRequest):
    removed_courses = models.ManyToManyField(SemesterCourse, related_name='removed_courses')
    added_courses = models.ManyToManyField(SemesterCourse, related_name='added_courses')

class RevisionRequest(StudentRegistrationRequest):
    course = models.ForeignKey(SemesterCourse, on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.TextField()

class EmergencyRemovalRequest(StudentRegistrationRequest):
    course = models.ForeignKey(SemesterCourse, on_delete=models.CASCADE)
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()

class StudentDeleteSemesterRequest(StudentRegistrationRequest):
    semester = models.ForeignKey(SemesterCourse, on_delete=models.CASCADE)
    student_explanations = models.TextField()
    result = models.CharField(max_length=100)
    educational_assistant_explanation = models.TextField()

class EnrollmentRequest(models.Model):
    APPROVAL_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    reason_text= models.TextField(blank=False)