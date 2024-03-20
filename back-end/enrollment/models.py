from django.db import models

class UnitSelectionRequest(models.Model):
    student = models.ForeignKey('accounts.Student' , on_delete = models.CASCADE)
    course = models.ForeignKey('education.SemesterCourse' , on_delete = models.CASCADE)
    status = models.CharField(max_length = 50)

class RevisionRequest(models.Model):
    student = models.ForeignKey('accounts.Student' , on_delete = models.CASCADE)
    course = models.ForeignKey('education.SemesterCourse' , on_delete = models.CASCADE)
    text = models.TextField()
    answer = models.TextField()
    
class AddRemoveRequest(models.Model):
    student = models.ForeignKey('accounts.Student' , on_delete = models.CASCADE)
    removed_courses = models.ManyToManyField('education.SemesterCourse' , on_delete = models.CASCADE)
    added_courses = models.ManyToManyField('education.SemesterCourse' , on_delete = models.CASCADE)
    status = models.CharField(max_length = 50)
    
class EmergencyRemovalRequest(models.Model):
    student = models.ForeignKey('accounts.Student' , on_delete = models.CASCADE)
    course = models.ForeignKey('education.SemesterCourse' , on_delete = models.CASCADE)
    status = models.CharField(max_length = 50)
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()
    
class EmploymentEducationRequest(models.Model):
    student = models.ForeignKey('accounts.Student' , on_delete = models.CASCADE)
    semester = models.ForeignKey('education.Semester' , on_delete = models.CASCADE)
    certificate_issuance_place = models.CharField(max_length = 255)
    study_employment_file = models.FileField(upload_to='enrollment/study_employment_files/' , null=True , blank=True)