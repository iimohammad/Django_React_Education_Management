from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import phone_validator
from education.models import Department, Major


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        UNSET = 'MF', 'Unset'

    user_number = models.CharField(max_length=255,blank=True)
    national_code = models.CharField(max_length=10,blank=True)
    birthday = models.DateField(null=True,blank=True)
    profile_image = models.ImageField(upload_to='accounts/profile_images/', null=True, blank=True)
    phone = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.UNSET)


class Teacher(models.Model):
    class Rank(models.TextChoices):
        INSTRUCTOR = 'I', 'Instructor'
        ASSISTANT_PROF = 'ASP', 'Assistant Professor'
        ASSOCIATE_PROF = 'ACP', 'Associate Professor'
        PROFESSOR = 'P', 'Professor'
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255)
    rank = models.CharField(max_length=3, choices=Rank.choices, default=Rank.INSTRUCTOR)
    department = models.ForeignKey('education.Department', on_delete=models.PROTECT)
    past_courses = models.ForeignKey('education.Course', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    entry_semester = models.ForeignKey('education.Semester', on_delete=models.PROTECT)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    entry_year = models.CharField(max_length=4)
    major = models.ForeignKey('education.Major', on_delete=models.PROTECT)
    advisor = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)
    military_service_status = models.CharField(max_length=100)
    year_of_study = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return str(self.user)


class EducationalAssistant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    field = models.ForeignKey(Major, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT,null=True)

    def __str__(self) -> str:
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return str(self.user)
