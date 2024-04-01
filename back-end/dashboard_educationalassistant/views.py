from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, views
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from accounts.models import Student, Teacher, EducationalAssistant
from education.models import StudentCourse
from .filters import StudentFilter, TeacherFilter
from .pagination import DefaultPagination
from .permissions import IsEducationalAssistant
from .serializers import StudentSerializer, TeacherSerializer, EducationalAssistantSerializer, StudentCourseSerializer
from accounts.serializers import UserProfileImageUpdateSerializer
from rest_framework.response import Response
from rest_framework import views, status
from django.db.models import Q
from django.core.exceptions import ValidationError






class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    search_fields = ['user__username', 'user__first_name', 'user__last_name',
                     'user__national_code',
                     ]
    ordering_fields = ['entry_semester']


class StudentApiView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsEducationalAssistant]


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TeacherFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    search_fields = ['title', 'description']
    ordering_fields = ['entry_semester']


class TeacherApiView(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsEducationalAssistant]


class EducationalAssistantChangeProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = EducationalAssistantSerializer
    permission_classes = [IsAuthenticated, IsEducationalAssistant]

    def get_object(self):
        return EducationalAssistant.objects.filter(user = self.request.user)


class StudentCoursesInProgress(generics.ListAPIView):
    serializer_class = StudentCourseSerializer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        student_id = self.kwargs['student_id']
        user = self.request.user
        if int(student_id) == user.student.id:            
            return StudentCourse.objects.filter(Q(student=student_id), Q(status='R'), Q(score__isnull=True) | Q(score__exact=''))

        elif hasattr(user, 'teacher'):
            students_with_advisor = Student.objects.filter(advisor=user.teacher)
            try:
                student_with_specific_id = students_with_advisor.get(id=student_id)
            except Student.DoesNotExist:
                raise ValidationError()
            return StudentCourse.objects.filter(Q(student=student_id), Q(status='R'), Q(score__isnull=True) | Q(score__exact=''))
        
        elif hasattr(user, 'educationalassistant') :
            student = Student.objects.get(id=student_id)  
            department_of_student = student.major.department
            if department_of_student == user.educationalassistant.field.department:
                return StudentCourse.objects.filter(Q(student=student_id), Q(status='R'), Q(score__isnull=True) | Q(score__exact=''))
            else:
                raise ValidationError()
        
        elif hasattr(user, 'adminuser'):
            return StudentCourse.objects.filter(Q(student=student_id), Q(status='R'), Q(score__isnull=True) | Q(score__exact=''))
        
        else:
                raise ValidationError()


class AcceptedStudentCourses(generics.ListAPIView):
    serializer_class = StudentCourseSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        user = self.request.user
        if int(student_id) == user.student.id:            
            return StudentCourse.objects.filter(student=user.student, is_pass=True)        

        elif hasattr(user, 'teacher'):
            students_with_advisor = Student.objects.filter(advisor=user.teacher)
            try:
                student_with_specific_id = students_with_advisor.get(id=student_id)
            except Student.DoesNotExist:
                raise ValidationError("You don't have access.")
            return StudentCourse.objects.filter(student=user.student, is_pass=True)        
        
        elif hasattr(user, 'educationalassistant') :
            student = Student.objects.get(id=student_id)  
            department_of_student = student.major.department
            if department_of_student == user.educationalassistant.field.department:
                return StudentCourse.objects.filter(student=user.student, is_pass=True)        
            else:
                raise ValidationError("You don't have access.")
        
        elif hasattr(user, 'adminuser'):
            return StudentCourse.objects.filter(student=user.student, is_pass=True)        
        else:
                raise ValidationError("You don't have access.")




class List_prof_approved():
    pass


class detail_prof_approved():
    pass


class prof_approved():
    pass



