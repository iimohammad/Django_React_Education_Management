from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentCourse

@receiver(post_save, sender=StudentCourse)
def update_student_gpa(sender, instance, created, **kwargs):
    if instance.score is not None and (created or instance.score != instance._original_score):
        student = instance.student
        student_courses = StudentCourse.objects.filter(student=student)
        total_score = sum(course.score for course in student_courses if course.score is not None)
        total_courses = student_courses.exclude(score=None).count()
        new_gpa = total_score / total_courses if total_courses > 0 else None
        student.gpa_student = new_gpa
        student.save(update_fields=['gpa_student'])
