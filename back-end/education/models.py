from django.db import models


class Department(models.Model):
    department_name = models.CharField(max_length=40)
    department_code = models.PositiveSmallIntegerField()
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
    department = models.ForeignKey(Department,on_delete = models.PROTECT)
    credit_num = models.PositiveSmallIntegerField()
    prerequisite = models.ManyToManyField('self' , related_name='prerequisites' , symmetrical=False)
    corequisite = models.ManyToManyField('self', related_name='corequisites' , symmetrical=False)

    def __str__(self):
        return self.course_name


# class Prerequisite(models.Model):
#     course = models.ForeignKey(Course, related_name='prerequisites', on_delete=models.CASCADE)
#     prerequisite = models.ForeignKey(Course, related_name='required_by', on_delete=models.CASCADE)


# class Corequisite(models.Model):
#     course = models.ForeignKey(Course, related_name='corequisites', on_delete=models.CASCADE)
#     corequisite = models.ForeignKey(Course, related_name='required_with', on_delete=models.CASCADE)


class Semester(models.Model):
    class SemesterType(models.TextChoices):
        Fall = 'F', 'Fall'
        Winter = 'W', 'Winter'
        Summer = 'S', 'Summer'

    name = models.CharField(max_length=100)
    start_semester = models.DateTimeField()
    end_semester = models.DateTimeField()
    semester_type = models.CharField(max_length=1, choices=SemesterType.choices, default=SemesterType.Fall)

    def __str__(self):
        return self.name


class SemesterUnitSelection(models.Model):
    semester = models.OneToOneField(Semester , on_delete=models.CASCADE , related_name = 'unit_selection')
    unit_selection_start = models.DateField()
    unit_selection_end = models.DateField()


class SemesterClass(models.Model):
    semester = models.OneToOneField(Semester , on_delete=models.CASCADE , related_name ='classes')
    classes_start = models.DateField()
    classes_end = models.DateField()


class SemesterAddRemove(models.Model):
    semester = models.OneToOneField(Semester , on_delete=models.CASCADE, related_name ='addremove')
    addremove_start = models.DateField()
    addremove_end = models.DateField()


class SemesterExam(models.Model):
    semester = models.OneToOneField(Semester , on_delete=models.CASCADE, related_name ='exam')
    exam_start = models.DateField()
    exam_end = models.DateField()


class SemesterEmergency(models.Model):
    semester = models.OneToOneField(Semester , on_delete=models.CASCADE, related_name ='emergency')
    emergency_remove_start = models.DateField()
    emergency_remove_end = models.DateField()


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
    instructor = models.ForeignKey('accounts.Teacher', on_delete=models.PROTECT)
    course_capacity = models.PositiveSmallIntegerField()
    corse_reserve_capasity = models.PositiveSmallIntegerField(default = 0)
    @property
    def remain_course_capacity(self):
        capacity = self.course_capacity
        occupied_capacity = StudentCourse.objects.filter(semester_course = self).count()
        return capacity-occupied_capacity
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
    semester_course = models.ForeignKey(SemesterCourse, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=REGISTERED)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    @property
    def is_pass(self):
        if self.score is not None and self.score >= 10:
            return True
        return False

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"