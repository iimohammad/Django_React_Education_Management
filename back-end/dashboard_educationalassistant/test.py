class Department(models.Model):
    department_name = models.CharField(max_length=40)


class Major(models.Model):
    major_name = models.CharField(max_length=30)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class EducationalAssistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    field = models.ForeignKey(Major, on_delete=models.PROTECT)


class Course(models.Model):
    course_name = models.CharField(max_length=40)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)


class SemesterCourse(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_days = models.ManyToManyField(Day)
    class_time_start = models.TimeField()
    class_time_end = models.TimeField()
    exam_datetime = models.DateTimeField()
    exam_location = models.CharField(max_length=100)
    instructor = models.ForeignKey(
        'accounts.Teacher', on_delete=models.PROTECT)
    course_capacity = models.PositiveSmallIntegerField()
    corse_reserve_capasity = models.PositiveSmallIntegerField(default=0)