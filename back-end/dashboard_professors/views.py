from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from education.models import Course, Semester, SemesterCourse
from accounts.permissions import IsTeacher
from .serializers import ShowSemestersSerializers


# Show Semesters with Details
class ShowSemestersView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = ShowSemestersSerializers
    queryset = Semester.objects.all()



# Professors Act as Teacher


# Professors Act as Advisor
# View to show students that this professor is her/his advisor 

# views that related to both of them
