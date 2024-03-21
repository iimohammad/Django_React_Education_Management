from django.db import models


class Department(models.Model):
    department_name = models.CharField(max_length=40)
    department_code = models.PositiveSmallIntegerField()
    year_established = models.DateField()
    department_location = models.TextField(blank=True)
    number_of_students = models.PositiveIntegerField()

    def __str__(self):
        return self.department_name


class Major(models.Model):
    class Level(models.TextChoices):
        BACHELOR = 'B', 'Bachelor'
        MASTER = 'M', 'Master'
        PHD = 'P', 'PhD'

    major_name = models.CharField(max_length=30)
    major_code = models.PositiveSmallIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    number_of_credits = models.PositiveIntegerField()
    level = models.CharField(max_length=1, choices=Level.choices, default=Level.BACHELOR)
    education_group = models.CharField(max_length=30)

    def __str__(self):
        return self.major_name


class Course(models.Model):
    course_name = models.CharField(max_length=40)
    course_code = models.PositiveSmallIntegerField()
    credit_num = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.course_name


class Prerequisite(models.Model):
    course = models.ForeignKey(Course, related_name='prerequisites', on_delete=models.CASCADE)
    prerequisite = models.ForeignKey(Course, related_name='required_by', on_delete=models.CASCADE)


class Corequisite(models.Model):
    course = models.ForeignKey(Course, related_name='corequisites', on_delete=models.CASCADE)
    corequisite = models.ForeignKey(Course, related_name='required_with', on_delete=models.CASCADE)


class Semester(models.Model):
    name = models.CharField(max_length=100)

    selection_start = models.DateTimeField()
    selection_end = models.DateTimeField()

    start_semester = models.DateTimeField()
    end_semester = models.DateTimeField()

    exam_start = models.DateTimeField()
    exam_end = models.DateTimeField()

    add_remove_start = models.DateTimeField()
    add_remove_end = models.DateTimeField()

    emergency_remove_start = models.DateTimeField()
    emergency_remove_end = models.DateTimeField()

    classes_start = models.DateTimeField()
    classes_end = models.DateTimeField()

    def __str__(self):
        return self.name


class SemesterCourse(models.Model):
    DAYS_CHOICES = [
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
    ]

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_days = models.CharField(max_length=20, choices=DAYS_CHOICES, blank=True, null=True)
    class_time = models.TimeField()
    exam_datetime = models.DateTimeField()
    exam_location = models.CharField(max_length=100)
    instructor = models.ForeignKey('accounts.Teacher', on_delete=models.CASCADE)
    class_capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.course_name} - {self.semester.name}"


class StudentCourse(models.Model):
    REGISTERED = 'R'
    PENDING = 'P'
    WITHDRAWN = 'W'
    
    STATUS_CHOICES = [
        (REGISTERED, 'Registered'),
        (PENDING, 'Pending'),
        (WITHDRAWN, 'Withdrawn'),
    ]

    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=REGISTERED)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    @property
    def is_pass(self):
        if self.score is not None and self.score >= 10:
            return True
        return False

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"
