from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import phone_validator


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        UNSET = 'MF', 'Unset'
    user_number = models.CharField(max_length = 255)
    national_code = models.CharField(max_lenth = 10)
    birthday = models.DateField()
    profile_image = models.ImageField(upload_to='accounts/profile_images/' , null=True , blank=True)
    phone = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    address = models.TextField(blank=True , null=True)
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.UNSET)

class Teacher(User):
    department = models.ForeignKey('education.department', on_delete = models.PROTECT)
    major = models.ForeignKey('education.Field' , on_delete = models.PROTECT)
    expertise = models.CharField(max_length = 255)
    rank = models.CharField(max_length = 255)
    past_courses = models.ForeignKey('education.Course' , on_delete = models.SET_NULL , null = True)

class Student(User):
    entry_semester = models.ForeignKey('education.Semester' , on_delete = models.PROTECT)
    gpa = models.DecimalField(max_digits = 4 , decimal_places = 2)
    entry_year = models.CharField(max_length = 4)
    major = models.ForeignKey('education.Field', on_delete = models.PROTECT)
    advisor = models.ForeignKey(Teacher , on_delete = models.SET_NULL,null= True)
    military_service_status = models.CharField(max_length = 100)
    year_of_study = models.PositiveSmallIntegerField()

class EducationalAssistant(User):
    field = models.ForeignKey('education.Field' , on_delete = models.PROTECT)