from django.db import models
from accounts.models import Student, Teacher
from education.models import Course, SemesterCourse , StudentCourse , Semester



APPROVAL_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]
class SemesterRegistrationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(
        max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)

    semester = models.ForeignKey(Semester , on_delete = models.PROTECT)
    requested_courses = models.ManyToManyField(
        Course , verbose_name='Requested_courses' , 
        blank=True)
    student_comment_for_requested_courses = models.TextField(null=True , blank = True)

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - \
            {self.semester.name}"

class UnitSelectionRequest(models.Model):
    semester_registration_request = models.OneToOneField(
        SemesterRegistrationRequest , on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    requested_courses = models.ManyToManyField(
        SemesterCourse, verbose_name='Requested_courses',
        blank=True)


class AddRemoveRequest(models.Model):
    semester_registration_request = models.ForeignKey(
        SemesterRegistrationRequest , on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    removed_courses = models.ManyToManyField(StudentCourse, related_name='removed_courses')
    added_courses = models.ManyToManyField(SemesterCourse, related_name='added_courses')

class RevisionRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    course = models.ForeignKey(StudentCourse, on_delete=models.PROTECT)
    text = models.TextField()
    answer = models.TextField()


class EmergencyRemovalRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    course = models.ForeignKey(StudentCourse, on_delete=models.PROTECT, null=True)
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - \
        {self.course.semester_course.semester.name}"


class StudentDeleteSemesterRequest(models.Model):
    semester_registration_request = models.ForeignKey(
        SemesterRegistrationRequest , on_delete=models.PROTECT, null=True)
    teacher_approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, 
                                               default='P')
    educational_assistant_approval_status = models.CharField(max_length=1, 
                                            choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    student_explanations = models.TextField()
    educational_assistant_explanation = models.TextField()

    def __str__(self):
        return f"{self.semester_registration_request.student.user.first_name} \
                {self.semester_registration_request.student.user.last_name} - \
                        {self.semester_registration_request.semester.name}"


class EnrollmentRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    reason_text= models.TextField(blank=False)


class EmploymentEducationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add = True)
    need_for = models.TextField()
    def __str__(self) -> str:
        return f"{self.student.user.first_name} {self.student.user.last_name}"
    