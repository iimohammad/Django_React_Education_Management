from django.contrib.auth.models import AbstractUser
from django.db import models
import logging
from education.models import Major
from django.conf import settings
from .validators import phone_validator , validate_national_code
from django.db.models.signals import post_save
from education.models import StudentCourse
from django.dispatch import receiver

logger = logging.getLogger(__name__)

# minio_client = Minio(
#     MINIO_SERVER_URL = settings.MINIO_SERVER_URL,
#     access_key=settings.MINIO_ROOT_USER,
#     secret_key=settings.MINIO_ROOT_PASSWORD,
#     secure=settings.MINIO_SECURE
# )

class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        UNSET = 'MF', 'Unset'

    user_number = models.CharField(max_length=255, blank=True)
    national_code = models.CharField(max_length=10, blank=True , 
                                    validators = [validate_national_code])
    birthday = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='accounts/profile_images/', null=True, blank=True)
    phone = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.UNSET)
    email = models.EmailField(unique=True, blank=False)

    def save(self, *args, **kwargs):
        logger.debug('DEBUG: Saving instance of Account: %s', self.username)
        logger.info('INFO: Saving instance of Account: %s', self.username)
        logger.warning('WARNING: Saving instance of Account: %s', self.username)
        logger.error('ERROR: Saving instance of Account: %s', self.username)
        logger.critical('CRITICAL: Saving instance of Account: %s', self.username)
        super().save(*args, **kwargs)


class Teacher(models.Model):
    class Rank(models.TextChoices):
        INSTRUCTOR = 'I', 'Instructor'
        ASSISTANT_PROF = 'ASP', 'Assistant Professor'
        ASSOCIATE_PROF = 'ACP', 'Associate Professor'
        PROFESSOR = 'P', 'Professor'

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    expertise = models.CharField(max_length=255)
    rank = models.CharField(
        max_length=3, choices=Rank.choices, default=Rank.INSTRUCTOR)
    department = models.ForeignKey(
        'education.Department', on_delete=models.PROTECT)
    can_be_advisor = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username


class Student(models.Model):
    MILITARY_CHOICES = [
        ('EP', 'Education Pardon'),  # معافیت تحصیلی
        ('P', 'Passed'),  # گزرانده
        ('E', 'Exempted'),  # معاف
        ('F','Finished')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    entry_semester = models.CharField(max_length=100)
    entry_year = models.CharField(max_length=4)
    major = models.ForeignKey('education.Major', on_delete=models.PROTECT)
    advisor = models.ForeignKey(
        'Teacher', on_delete=models.SET_NULL, null=True)
    military_service_status = models.CharField(max_length=2, choices=MILITARY_CHOICES, default='EP')
    year_of_study = models.PositiveSmallIntegerField()

    @property
    def gpa(self):
        # Calculate GPA based on scores of registered courses
        registered_courses = StudentCourse.objects.filter(student=self)
        if registered_courses.exists():
            gpa = registered_courses.aggregate(Avg('score'))['score__avg']
            return gpa
        return None

    @property
    def calculate_total_credits(self):
        # Calculate total credits taken by the student
        total_credits = StudentCourse.objects.filter(student=self).aggregate(Sum('semester_course__course__credit_num'))['semester_course__course__credit_num__sum']
        if total_credits is not None:
            return total_credits
        return 0

    @property
    def category_of_student_grade(self):
        if self.gpa >= 17:
            return 'A'
        elif self.gpa < 17 and self.gpa >= 14:
            return 'B'
        elif self.gpa <14 and self.gpa >=12:
            return 'C'
        else:
            return 'D'
        
    def save(self, *args, **kwargs):
        # Update GPA and total credits when saving the student object
        self.gpa = self.calculate_gpa()
        self.total_credits = self.calculate_total_credits()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return str(self.user)

@receiver(post_save, sender=StudentCourse)
def update_student_info(sender, instance, **kwargs):
    student = instance.student
    # Recalculate the student's GPA and total credits
    student.gpa = student.calculate_gpa()
    student.total_credits = student.calculate_total_credits()
    student.save()



class EducationalAssistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    field = models.ForeignKey(Major, on_delete=models.PROTECT)

    def __str__(self) -> str:
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return str(self.user)


class AdminUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, related_name='adminuser')
