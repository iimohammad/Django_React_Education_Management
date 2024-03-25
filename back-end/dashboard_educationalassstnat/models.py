from django.db import models
from accounts.models import User, Teacher
from education.models import TermCourse

class ApprovedCourse(models.Model):
    Title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class SemesterCourse(models.Model):
    Title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    semester = models.CharField(max_lenght=20)
    created_at = models.DateTimeField(auto_now_add=True)
    week_day_course = models.CharField(max_length=50)
    exam_location = models.CharField(max_length=100)  
    exam_time = models.TimeField()  

class EducationAssistant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField()
    contact_number = models.CharField(max_length=15)

class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(TermCourse, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'

    ACTION_CHOICES = [
        (CREATE, 'Create'),
        (UPDATE, 'Update'),
        (DELETE, 'Delete'),

    ]
