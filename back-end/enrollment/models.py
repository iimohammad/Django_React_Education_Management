from django.db import models

from accounts.models import User,Student

class StudeRequestRegistration(models.Model):
    student = models.ForeignKey(Student,on_delete= models.PROTECT)
    code = models.PositiveSmallIntegerField()
    status = models.BooleanField(default=False)

class SemesterRegistrationRequest(StudeRequestRegistration):
    requested_courses = models.ManyToManyField('Course', verbose_name='Requested_courses')
    

class AddRemoveRequest(StudeRequestRegistration):
    removed_courses = models.ManyToManyField('education.SemesterCourse' , on_delete = models.CASCADE)
    added_courses = models.ManyToManyField('education.SemesterCourse' , on_delete = models.CASCADE)


class RevisionRequest(StudeRequestRegistration):
    course = models.ForeignKey('education.SemesterCourse' , on_delete = models.CASCADE)
    text = models.TextField()
    answer = models.TextField()


class EmergencyRemovalRequest(StudeRequestRegistration):
    course = models.ForeignKey('education.SemesterCourse' , on_delete = models.CASCADE)
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()
    

class Student_DeleteSemesterRequest(StudeRequestRegistration):
    semester = models.ForeignKey('education.Semester' , on_delete = models.CASCADE)
    student_explantions = models.TextField()
    result = models.CharField() # Change to choises 
    educational_assistant_explanation = models.TextField()
     

