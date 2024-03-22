from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import phone_validator


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        UNSET = 'MF', 'Unset'

    user_number = models.CharField(max_length=255)
    national_code = models.CharField(max_length=10)
    birthday = models.DateField(null=True)
    profile_image = models.ImageField(upload_to='accounts/profile_images/', null=True, blank=True)
    phone = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.UNSET)


class Teacher(User):
    expertise = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    department = models.ForeignKey('education.Department', on_delete=models.PROTECT)
    past_courses = models.ForeignKey('education.Course', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Professor {self.first_name} {self.last_name}'


class Student(User):
    entry_semester = models.ForeignKey('education.Semester', on_delete=models.PROTECT)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    entry_year = models.CharField(max_length=4)
    major = models.ForeignKey('education.Major', on_delete=models.PROTECT)
    advisor = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)
    military_service_status = models.CharField(max_length=100)
    year_of_study = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class EducationalAssistant(User):
    field = models.ForeignKey('education.Major', on_delete=models.PROTECT)
    department = models.ForeignKey('education.Department', on_delete=models.PROTECT)

    def __str__(self):
        if self.gender == 'M':
            return f'Mr. {self.first_name} {self.last_name}'
        elif self.gender == 'F':
            return f'Ms. {self.first_name} {self.last_name}'
        else:
            return f'{self.first_name} {self.last_name}'
