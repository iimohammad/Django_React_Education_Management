from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from accounts.models import EducationalAssistant, Student, Teacher
from accounts.permissions import IsAdmin
from accounts.serializers import (EducationalAssistantSerializer,
                                  StudentSerializer, TeacherSerializers)
from education.models import Course, Department, Semester, SemesterCourse
from education.serializers import (CourseSerializers, DepartmentSerializers,
                                   SemesterCourseSerializers,
                                   SemesterSerializers)


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
    permission_classes = [IsAuthenticated, IsAdmin, IsAdminUser]
    serializer_class = CourseSerializers


class SemesterCourseViewSet(viewsets.ModelViewSet):
    queryset = SemesterCourse.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin, IsAdminUser]
    serializer_class = SemesterCourseSerializers
