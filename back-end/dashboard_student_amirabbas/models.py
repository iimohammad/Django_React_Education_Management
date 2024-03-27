from django.db import models
from accounts.models import Student, Teacher
from education.models import SemesterCourse , StudentCourse , Semester


class BaseStudentRegistrationRequest():
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)

class AddRemoveRequest(models.Model , BaseStudentRegistrationRequest):
    removed_courses = models.ManyToManyField(StudentCourse, related_name='removed_courses')
    added_courses = models.ManyToManyField(SemesterCourse, related_name='added_courses')


class SemesterRegistrationRequest(models.Model, BaseStudentRegistrationRequest):
    requested_courses = models.ManyToManyField(SemesterCourse, verbose_name='Requested_courses')



class EmergencyRemovalRequest(models.Model , BaseStudentRegistrationRequest):
    course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()


class RemoveDuplicateRequest(models.Model , BaseStudentRegistrationRequest):
    removed_duplicates = models.ManyToManyField(StudentCourse, related_name='removed_duplicates')


class Reminder(models.Model , BaseStudentRegistrationRequest):
    message = models.TextField()
    created_at =  models.DateTimeField(auto_now_add=True)

class CourseRegistrationCancellation(models.Model , BaseStudentRegistrationRequest):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ManyToManyField(SemesterCourse, on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()
