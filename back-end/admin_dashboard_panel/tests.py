from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .pagination import DefaultPagination
from .versioning import DefualtVersioning
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from accounts.models import EducationalAssistant, Student, Teacher, User
from accounts.permissions import IsAdmin
from accounts.serializers import EducationalAssistantSerializer, StudentSerializer
from education.models import Course, Department, Semester, SemesterCourse
from education.serializers import CourseSerializers, DepartmentSerializers, SemesterSerializers, SemesterCourseSerializers

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return TeacherSerializers


class EducationalAssistantViewSet(viewsets.ModelViewSet):
    queryset = EducationalAssistant.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return EducationalAssistantSerializer
        


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return StudentSerializer
    


# Department
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return DepartmentSerializers
    



# Semester
class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return SemesterSerializers
        



# Use in two pannels
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return CourseSerializers

class SemesterCourseViewSet(viewsets.ModelViewSet):
    queryset = SemesterCourse.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return SemesterCourseSerializers
