from django.shortcuts import render
from rest_framework import viewsets
from accounts.models import Teacher, EducationalAssistant,Student
from education.models import Department, Semester, SemesterCourse
from accounts.serializers import TeacherSerializers,EducationalAssistantSerializer,StudentSerializer
from education.serializers import DepartmentSerializers, SemesterCourseSerializers,SemesterSerializers
from education.serializers import CourseSerializers
from education.models import Course
from accounts.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated,IsAdminUser


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = TeacherSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EducationalAssistantViewSet(viewsets.ModelViewSet):
    queryset = EducationalAssistant.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = EducationalAssistantSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


StudentSerializer
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Department
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = DepartmentSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Semester
class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = SemesterSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Use in two pannels 
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin,IsAdminUser]
    serializer_class = CourseSerializers

class SemesterCourseViewSet(viewsets.ModelViewSet):
    queryset = SemesterCourse.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin,IsAdminUser]
    serializer_class = SemesterCourseSerializers