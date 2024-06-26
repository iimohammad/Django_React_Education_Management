from django.contrib.auth.models import AbstractUser
from django.db import models
import logging
from education.models import Major
from config.settings import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
)
from .validators import phone_validator , validate_national_code


logger = logging.getLogger(__name__)




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
        ('F', 'Finished')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    entry_semester = models.CharField(max_length=100)
    entry_year = models.CharField(max_length=4)
    major = models.ForeignKey('education.Major', on_delete=models.PROTECT)
    advisor = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)
    military_service_status = models.CharField(max_length=2, choices=MILITARY_CHOICES, default='EP')
    year_of_study = models.PositiveSmallIntegerField()
    gpa_student = models.PositiveBigIntegerField(blank=True,null=True)

    @property
    def gpa(self):
        return self.gpa_student


    @property
    def category_of_student_grade(self):
        if self.gpa is None:
            return 'B'
        if self.gpa is not None:
            if self.gpa >= 17:
                return 'A'
            elif self.gpa >= 14:
                return 'B'
            elif self.gpa >= 12:
                return 'C'
        return 'D'
        
    def save(self, *args, **kwargs):
        # Update GPA and total credits when saving the student object
        self.full_clean()  # Ensure model validation before saving
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return str(self.user)

# @receiver(post_save, sender=StudentCourse)
# def update_student_info(sender, instance, **kwargs):
#     student = instance.student
#     # Recalculate the student's GPA and total credits
#     # student.gpa = student.calculate_gpa()
#     student.total_credits = student.calculate_total_credits()
#     student.save()



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
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"