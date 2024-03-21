from django.db import models

from accounts.models import User

class UnitSelectionRequest(models.Model):
    student = models.ForeignKey(User , on_delete = models.CASCADE)
    course = models.ForeignKey('education.SemesterCourse' , on_delete = models.CASCADE)
    status = models.CharField(max_length = 50)

class RevisionRequest(models.Model):
    student = models.ForeignKey(User , on_delete = models.CASCADE)
    course = models.ForeignKey('education.SemesterCourse' , on_delete = models.CASCADE)
    text = models.TextField()
    answer = models.TextField()
    
class AddRemoveRequest(models.Model):
    student = models.ForeignKey(User , on_delete = models.CASCADE)
    removed_courses = models.ManyToManyField('education.SemesterCourse' , on_delete = models.CASCADE)
    added_courses = models.ManyToManyField('education.SemesterCourse' , on_delete = models.CASCADE)
    status = models.CharField(max_length = 50)
    
class EmergencyRemovalRequest(models.Model):
    student = models.ForeignKey(User , on_delete = models.CASCADE)
    course = models.ForeignKey('education.SemesterCourse' , on_delete = models.CASCADE)
    status = models.CharField(max_length = 50)
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()
    
class EmploymentEducationRequest(models.Model):
    student = models.ForeignKey(User , on_delete = models.CASCADE)
    semester = models.ForeignKey('education.Semester' , on_delete = models.CASCADE)
    certificate_issuance_place = models.CharField(max_length = 255)
    study_employment_file = models.FileField(upload_to='enrollment/study_employment_files/' , null=True , blank=True)

class Student_DeleteSemesterRequest(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    semester = models.ForeignKey('education.Semester' , on_delete = models.CASCADE)
    student_explantions = models.TextField()
    


class AssistanceResponse(models.Model):
    response_to = models.ForeignKey(Student_DeleteSemesterRequest,on_delete=models.CASCADE)
    assistance = student = models.ForeignKey(User,on_delete=models.CASCADE)
    educations_assistance_explanations = models.TextField()


