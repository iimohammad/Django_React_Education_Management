# Assuming you have already set up your Django project and models

# 1. Install the necessary packages:
# pip install graphene-django

# 2. Create a schema.py file in your app (e.g., myapp/schema.py):

# myapp/schema.py
import graphene
from graphene_django.types import DjangoObjectType
from education.models import Course, Semester, SemesterCourse
from django.utils import timezone


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class SemesterType(DjangoObjectType):
    class Meta:
        model = Semester


class SemesterCourseType(DjangoObjectType):
    class Meta:
        model = SemesterCourse


class Query(graphene.ObjectType):
    current_semester_courses = graphene.List(SemesterCourseType)

    def resolve_current_semester_courses(self, info):
        # Get the current semester (you can adjust this logic as needed)
        current_semester = Semester.objects.filter(
            start_semester__lte=timezone.now(),
            end_semester__gte=timezone.now(),
        ).first()

        if current_semester:
            return SemesterCourse.objects.filter(semester=current_semester)
        else:
            return None

schema = graphene.Schema(query=Query)
