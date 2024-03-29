from django.db import models

from accounts.models import Student


class EmploymentEducationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(
        'education.Semester', on_delete=models.CASCADE)
    certificate_issuance_place = models.CharField(max_length=255)
    study_employment_file = models.FileField(
        upload_to='dashboard_student/study_employment_files/', null=True, blank=True)
