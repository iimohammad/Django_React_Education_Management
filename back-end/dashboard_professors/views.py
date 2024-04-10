import csv
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Student, Teacher, User
from .pagination import DefaultPagination
from .versioning import DefualtVersioning
from accounts.permissions import IsTeacher
from dashboard_professors.queryset import get_student_queryset
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from education.models import Semester, SemesterCourse, StudentCourse
from education.serializers import StudentCourseSerializer
from .tasks import send_approval_email
from .serializers import (
    AddRemoveRequestViewSerializers,
    EmergencyRemovalRequestSerializers,
    RevisionRequestSerializers,
    SemesterCourseSerializer,
    SemesterRegistrationRequestSerializers,
    ShowSemestersSerializers,
    StudentDeleteSemesterRequestSerializers,
    UnitSelectionRequestSerializers,
)
from accounts.serializers import (
    StudentSerializer,
    UserProfileImageUpdateSerializer,
    TeacherSerializer
)
from dashboard_student.models import EmploymentEducationRequest
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from .serializers import (
    EmploymentEducationConfirmationSerializer,
)


class BaseConfig():
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning


# General Tasks
class ShowProfileAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated] 
    versioning_class = DefualtVersioning
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return TeacherSerializer
    def get_object(self):
        user = self.request.user

        try:
            # Get the teacher instance associated with the current user
            teacher = Teacher.objects.get(user=user)
            return teacher
        except Teacher.DoesNotExist:
            # Handle the case where the user is not a teacher
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'error': 'User is not a teacher'}, status=404)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserProfileImageView(UpdateAPIView, BaseConfig):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsTeacher]
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return UserProfileImageUpdateSerializer
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# Tasks of Teachers
class ShowSemestersView(viewsets.ReadOnlyModelViewSet, BaseConfig):
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Semester.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return ShowSemestersSerializers
    @action(detail=True, methods=['get'],
            name='Show All Course of This Semester')
    def all_semester_courses(self, request, pk=None):
        semester = self.get_object()
        serializer = self.get_serializer(semester)

        # Retrieve courses associated with the semester
        courses = SemesterCourse.objects.filter(semester=semester)
        course_serializer = SemesterCourseSerializer(courses, many=True)

        return Response({'semester': serializer.data,
                         'courses': course_serializer.data})


# Evaluate Students
class SemesterCourseViewSet(viewsets.ReadOnlyModelViewSet, BaseConfig):
    permission_classes = [IsAuthenticated, IsTeacher]
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return SemesterCourseSerializer
    def get_queryset(self):
        teacher = self.request.user.teacher
        queryset = SemesterCourse.objects.filter(instructor=teacher)
        return queryset

    @action(detail=True, methods=['post'], name='Evaluate Students')
    def evaluate_students(self, request, pk=None):
        semester_course = self.get_object()
        data = request.data.get('student_scores', [])

        for entry in data:
            student_id = entry.get('student_id')
            score = entry.get('score')
            action = entry.get('action')

            # Fetch the student course instance
            student_course = StudentCourse.objects.filter(
                semester_course=semester_course, student_id=student_id).first()

            if action == 'add':
                if student_course:
                    # Update score if student course exists
                    student_course.score = score
                    student_course.save()
            elif action == 'change':
                # Update score if student course exists
                if student_course:
                    student_course.score = score
                    student_course.save()

        return Response(
            {'message': 'Student scores updated successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], name='Show Score Students')
    def score_students(self, request, pk=None):
        semester_course = self.get_object()
        students = StudentCourse.objects.filter(
            semester_course=semester_course)
        serializer = StudentCourseSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], name='Send CSV file Evaluation')
    def evaluate_students_by_CSV(self, request, pk=None):
        semester_course = self.get_object()
        data_file = request.FILES.get('file')

        if data_file:
            # Assuming CSV file has 'student_id' and 'score' columns
            csv_data = csv.DictReader(data_file)
            for row in csv_data:
                student_id = row.get('student_id')
                score = row.get('score')

                # Fetch or create StudentCourse instance
                student_course, created = StudentCourse.objects.get_or_create(
                    semester_course=semester_course,
                    student_id=student_id,
                    defaults={'score': score}
                )

                # If not created, update score
                if not created:
                    student_course.score = score
                    student_course.save()

            return Response(
                {'message': 'Student scores updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No file uploaded'},
                            status=status.HTTP_400_BAD_REQUEST)


class RevisionRequestView(generics.UpdateAPIView, BaseConfig):
    permission_classes = [IsAuthenticated, IsTeacher]
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return RevisionRequestSerializers
    def get_queryset(self):
        teacher = self.request.user.teacher
        queryset = SemesterCourse.objects.filter(instructor=teacher)
        return queryset


# Adviser Tasks APIs
class ShowMyStudentsVeiw(generics.GenericAPIView, ListModelMixin, BaseConfig):
    permission_classes = [IsAuthenticated, IsTeacher]
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return StudentSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return get_student_queryset(self.request)


class UnitSelectionRequestView(generics.UpdateAPIView, BaseConfig):
    permission_classes = [IsTeacher, IsAuthenticated]

    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return UnitSelectionRequestSerializers
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return get_student_queryset(self.request)


class SemesterRegistrationRequestView(generics.UpdateAPIView, BaseConfig):
    permission_classes = [IsTeacher, IsAuthenticated] 
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return SemesterRegistrationRequestSerializers
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return get_student_queryset(self.request)


class AddRemoveRequestView(generics.UpdateAPIView, BaseConfig):
    permission_classes = [IsTeacher, IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return AddRemoveRequestViewSerializers
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return get_student_queryset(self.request)


class EmergencyRemovalRequestView(generics.UpdateAPIView, BaseConfig):
    permission_classes = [IsTeacher, IsAuthenticated]
    
    # def get_serializer_class(self):
    #   if self.request.version == 'v1':
    #       return ...
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return get_student_queryset(self.request)


class StudentDeleteSemesterRequestView(generics.UpdateAPIView, BaseConfig):
    permission_classes = [IsTeacher, IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return StudentDeleteSemesterRequestSerializers
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return get_student_queryset(self.request)


class EmploymentEducationConfirmationAPI(
    generics.UpdateAPIView,
    BaseConfig,
    generics.ListAPIView
):
    permission_classes = [IsTeacher, IsAuthenticated]

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return EmploymentEducationConfirmationSerializer

    queryset = EmploymentEducationRequest.objects.filter(approval_status='P')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        approval_status_changed = instance.approval_status != serializer.validated_data['approval_status']
        serializer.save()

        if approval_status_changed and serializer.validated_data['approval_status'] == 'A':
            send_approval_email.delay(instance.student.user.email)
            
        return Response(serializer.data)