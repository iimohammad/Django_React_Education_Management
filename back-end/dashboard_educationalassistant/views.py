from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from accounts.models import Student, Teacher, EducationalAssistant
from education.models import StudentCourse, SemesterCourse
from .filters import StudentFilter, TeacherFilter
from .pagination import DefaultPagination
from accounts.permissions import IsEducationalAssistant
from .serializers import StudentSerializer, TeacherSerializer, EducationalAssistantSerializer, StudentCourseSerializer, SemesterCourseSerializer
from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404







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




from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class EducationAssistantApprovedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    serializer_class = SemesterCourseSerializer
    
    def list(self, request):
        educationalassistant = self.request.user.educationalassistant
        queryset = SemesterCourse.objects.filter(instructor__department=educationalassistant)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], name='Evaluate Students')
    def evaluate_students(self, request, pk=None):
        semester_course = self.get_semester_course(pk)
        data = request.data.get('student_scores', [])

        for entry in data:
            student_id = entry.get('student_id')
            score = entry.get('score')
            action = entry.get('action')

            # Fetch the student course instance
            student_course = StudentCourse.objects.filter(
                semester_course=semester_course, student_id=student_id).first()

            if action in ['add', 'change']:
                if student_course:
                    # Update score if student course exists
                    student_course.score = score
                    student_course.save()

        return Response({'message': 'Student scores updated successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], name='Show Score Students')
    def score_students(self, request, pk=None):
        semester_course = self.get_semester_course(pk)
        students = StudentCourse.objects.filter(semester_course=semester_course)
        serializer = StudentCourseSerializer(students, many=True)
        return Response(serializer.data)
    
    def get_semester_course(self, pk):
        educationalassistant = self.request.user.educationalassistant
        try:
            return SemesterCourse.objects.get(id=pk, instructor__department=educationalassistant)
        except SemesterCourse.DoesNotExist:
            raise Http404
