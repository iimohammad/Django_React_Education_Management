from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Department(models.Model):
    department_name = models.CharField(max_length=40, unique=True)
    department_code = models.PositiveSmallIntegerField(unique=True)
    year_established = models.DateField()
    department_location = models.TextField(blank=True)

    def __str__(self):
        return self.department_name


class Major(models.Model):
    class Level(models.TextChoices):
        BACHELOR = 'B', 'Bachelor'
        MASTER = 'M', 'Master'
        PHD = 'P', 'PhD'

    major_name = models.CharField(max_length=30)
    major_code = models.PositiveSmallIntegerField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    number_of_credits = models.PositiveIntegerField()
    level = models.CharField(
        max_length=1, choices=Level.choices, default=Level.BACHELOR)
    education_group = models.CharField(max_length=30)

    def __str__(self):
        return self.major_name


class Course(models.Model):
    COURSE_TYPES = [
        ('L', 'Laboratory'),
        ('R', 'Research'),
        ('I', 'Internship'),
        ('A', 'Activity '),
        ('G', 'General'),
        ('B', 'Basic'),
    ]
    AVAILABLITY_TYPES = [
        ('A', 'Available'),
        ('D', 'Deleted'),
    ]
    course_name = models.CharField(max_length=40)
    course_code = models.PositiveSmallIntegerField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    major = models.ForeignKey(Major, on_delete=models.PROTECT)
    credit_num = models.PositiveSmallIntegerField()
    course_type = models.CharField(
        max_length=1, choices=COURSE_TYPES)
    availablity = models.CharField(
        max_length=1, choices=AVAILABLITY_TYPES)
    def __str__(self):
        return self.course_name


class Prerequisite(models.Model):
    course = models.ForeignKey(
        Course, related_name='prerequisites', on_delete=models.CASCADE)
    prerequisite = models.ForeignKey(
        Course, related_name='required_by', on_delete=models.CASCADE)

    def __str__(self):
        return self.course.course_name


class Requisite(models.Model):
    course = models.ForeignKey(
        Course, related_name='requisites', on_delete=models.CASCADE)
    requisite = models.ForeignKey(
        Course, related_name='required_with', on_delete=models.CASCADE)

    def __str__(self):
        return self.course.course_name


class Semester(models.Model):
    class SemesterType(models.TextChoices):
        Fall = 'F', 'Fall'
        Winter = 'W', 'Winter'
        Summer = 'S', 'Summer'

    name = models.CharField(max_length=100 , unique = True)
    start_semester = models.DateField()
    end_semester = models.DateField()
    semester_type = models.CharField(
        max_length=1, choices=SemesterType.choices, default=SemesterType.Fall)

    def __str__(self):
        return self.name


class SemesterUnitSelection(models.Model):
    semester = models.OneToOneField(
        Semester, on_delete=models.CASCADE, related_name='unit_selection')
    unit_selection_start = models.DateField()
    unit_selection_end = models.DateField()


class SemesterClass(models.Model):
    semester = models.OneToOneField(
        Semester, on_delete=models.CASCADE, related_name='classes')
    classes_start = models.DateField()
    classes_end = models.DateField()


class SemesterAddRemove(models.Model):
    semester = models.OneToOneField(
        Semester, on_delete=models.CASCADE, related_name='addremove')
    addremove_start = models.DateField()
    addremove_end = models.DateField()


class SemesterExam(models.Model):
    semester = models.OneToOneField(
        Semester, on_delete=models.CASCADE, related_name='exams')
    exam_start = models.DateField()
    exam_end = models.DateField()


class SemesterEmergency(models.Model):
    semester = models.OneToOneField(
        Semester, on_delete=models.CASCADE, related_name='emergency')
    emergency_remove_start = models.DateField()
    emergency_remove_end = models.DateField()

def create_week_days(sender, **kwargs):
        for day, _ in Day.DAY_CHOICES:
            Day.objects.get_or_create(name=day)
class Day(models.Model):
    DAY_CHOICES = [
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
    ]
    name = models.CharField(max_length=20, choices=DAY_CHOICES, unique=True)

    def __str__(self):
        return str(self.name)
    
    @receiver(post_migrate)
    def on_migrate(sender, **kwargs):
        create_week_days(sender, **kwargs)
class SemesterCourse(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_days = models.ManyToManyField(Day)
    class_time_start = models.TimeField()
    class_time_end = models.TimeField()
    exam_datetime = models.DateTimeField(null=True , blank = True)
    exam_location = models.CharField(max_length=100 , null=True , blank = True)
    instructor = models.ForeignKey(
        'accounts.Teacher', on_delete=models.PROTECT)
    course_capacity = models.PositiveSmallIntegerField()
    corse_reserve_capasity = models.PositiveSmallIntegerField(default=0)

    @property
    def remain_course_capacity(self):
        return self.course_capacity - StudentCourse.objects.filter(
            semester_course = self).count()

    def __str__(self):
        return f"{self.course.course_name} - {self.semester.name}"


class StudentCourse(models.Model):
    FINALREGISTERED = 'F'
    REGISTERED = 'R'
    PENDING = 'P'
    WITHDRAWN = 'W'
    DELETED = 'D'

    STATUS_CHOICES = [
        (FINALREGISTERED , 'FinalRegistered'),
        (REGISTERED, 'Registered'),
        (PENDING, 'Pending'),
        (WITHDRAWN, 'Withdrawn'),
        (DELETED, 'Deleted'),
    ]

    student = models.ForeignKey('accounts.Student', on_delete=models.PROTECT)
    semester_course = models.ForeignKey(
        SemesterCourse, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=REGISTERED)
    score = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    @property
    def is_pass(self):
        if self.score is not None and self.score >= 10:
            return True
        return False


    def __str__(self):
        return f"{self.semester_course.course.course_name} \
        - {self.semester_course.semester.name}"

    class Meta:
        unique_together = [["student", "semester_course"]]

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - \
        {self.semester_course.semester.name}"
