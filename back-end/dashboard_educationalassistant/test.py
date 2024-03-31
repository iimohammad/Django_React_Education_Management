class SemesterCourse(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_days = models.ManyToManyField(Day)


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
    semester_course = models.ForeignKey(
        SemesterCourse, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=REGISTERED)
    score = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

# Assuming you have the student and semester instances
student_instance = ...  # Your student instance
semester_instance = ...  # Your semester instance

# Retrieve all StudentCourse instances related to the given student and semester
student_courses = StudentCourse.objects.filter(
    student=student_instance,
    semester_course__semester=semester_instance
)