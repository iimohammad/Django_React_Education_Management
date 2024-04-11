from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

APPROVAL_CHOICES = [
    ('P', 'Pending'),
    ('A', 'Approved'),
    ('R', 'Rejected'),
]

UnitSelection_APPROVAL_CHOICES = [
    ('A', 'Registered'),
    ('R', 'Reserved'),
    ('C', "NeedChange"),
    ('P', 'Approved'),
    ('D', 'DeletedSemester'),
]


class SemesterRegistrationRequest(models.Model):
    student = models.ForeignKey('accounts.Student',  on_delete=models.CASCADE)
    approval_status = models.CharField(
        max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    semester = models.ForeignKey('education.Semester',  on_delete=models.CASCADE)
    requested_courses = models.ManyToManyField(
        'education.Course', verbose_name='Requested_courses',
        blank=True)
    teacher_comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - \
            {self.semester.name}"


class UnitSelectionRequest(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    semester_registration_request = models.OneToOneField(
        SemesterRegistrationRequest, on_delete=models.PROTECT
    )
    approval_status = models.CharField(max_length=1, choices=UnitSelection_APPROVAL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    request_course = models.OneToOneField(
        'education.SemesterCourse',
        on_delete=models.CASCADE,
        default=None
    )

    def save(self, *args, **kwargs):
        self.clean()

        if self.student.category_of_student_grade:
        #     # Define the maximum credit limit for each category
            max_credit_limits = {
                'A': 24,
                'B': 20,
                'C': 17,
                'D': 14,

            }
            max_credit_limit = max_credit_limits.get(self.student.category_of_student_grade, 0)
        #     requested_courses_credits_sum = self.student.unit_selection_request.aggregate(
        #         total_credits=models.Sum('request_course__semestercourse__credit_num')
        #     )['total_credits'] or 0

        # #     if requested_courses_credits_sum + self.request_course.course.credit_num > max_credit_limit:
        # #         raise ValidationError(
        # #             f'Cannot request more courses. Maximum allowed credit limit for Category '
        # #             f'{self.student.category_of_student_grade} students is {max_credit_limit}.'
        # #         )

        prerequisites = self.request_course.course.prerequisites.all()
        for prerequisite_course in prerequisites:
            if not self.student.studentcourse_set.filter(
                    semester_course__course=prerequisite_course,
                    score__gte=10
            ).exists():
                raise ValidationError(
                    f'Cannot request {self.request_course.course} because prerequisite course {prerequisite_course} has not been passed.'
                )

        requisites = self.request_course.course.requisites.all()
        if requisites and not self.student.studentcourse_set.filter(semester_course__course__in=requisites,
                                                                    status='R').exists():
            self.warning_message = 'Warning: Requisite course is not selected.'
        if UnitSelectionRequest.objects.filter(
                semester_registration_request=self.semester_registration_request,
                request_course=self.request_course
        ).exists():
            raise ValidationError(('Unit selection request for this course already exists.'))
        
        if self.request_course.studentcourse_set.filter(student=self.student, score__gte=10).exists():
            raise ValidationError(('Cannot request a course that has already been passed.'))

        super().save(*args, **kwargs)


class QueuedRequest(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    semester_registration_request = models.ForeignKey(
        SemesterRegistrationRequest, on_delete=models.PROTECT
    )
    request_course = models.ForeignKey(
        'education.SemesterCourse',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


class AddRemoveRequest(UnitSelectionRequest):
    pass


class RevisionRequest(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.PROTECT)
    teacher_approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES,
                                               default='P')
    educational_assistant_approval_status = models.CharField(max_length=1,
                                                             choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('education.StudentCourse', on_delete=models.PROTECT)
    text = models.TextField()
    answer = models.TextField(null=True, blank=True)


class EmergencyRemovalRequest(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('education.StudentCourse', on_delete=models.PROTECT, null=True)
    student_explanation = models.TextField()

    def __str__(self):
        return (
            f"{self.student.user.first_name} "
            f"{self.student.user.last_name} - "
            f"{self.course.semester_course.semester.name}"
        )
    # def save(self, *args, **kwargs):
    #     existing_request = EmergencyRemovalRequest.objects.filter(
    #         student=self.student,
    #         course__semester_course__semester__emergency__emergency_remove_start__lte=timezone.now(),
    #         course__semester_course__semester__emergency__emergency_remove_end__gte=timezone.now()
    #     ).exists()

    #     if existing_request:
    #         raise ValidationError(
    #             "A student can only create one EmergencyRemovalRequest per semester."
    #             )

    #     super().save(*args, **kwargs)


class StudentDeleteSemesterRequest(models.Model):
    semester_registration_request = models.ForeignKey(
        SemesterRegistrationRequest, on_delete=models.PROTECT, null=True)
    teacher_approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES,
                                               default='P')
    educational_assistant_approval_status = models.CharField(max_length=1,
                                                             choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    student_explanations = models.TextField(null=True, blank=True)
    educational_assistant_explanation = models.TextField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.semester_registration_request.student.user.first_name} "
            f"{self.semester_registration_request.student.user.last_name} - "
            f"{self.semester_registration_request.semester.name}"
        )


class EmploymentEducationRequest(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.PROTECT)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    need_for = models.TextField()

    def __str__(self) -> str:
        return f"{self.student.user.first_name} {self.student.user.last_name}"
