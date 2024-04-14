import json
from rest_framework import viewsets, mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from .permissions import (
    IsStudent, 
    HavePermosionForUnitSelectionForLastSemester,
    HavePermissionBasedOnUnitSelectionTime,
    HavePermissionBasedOnAddAndRemoveTime,
    HavePermssionEmoloymentDegreeTime,
)
from accounts.models import Student
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import (
    CourseSerializer,
    EmergencyRemovalRequestSerializer,
    EmploymentEducationRequestSerializer,
    ExamStudentCourseSerializer,
    ProfileStudentSerializer,
    RevisionRequestSerializer,
    SemesterCourseSerializer,
    SemesterRegistrationRequestSerializer,
    StudentCourseSerializer,
    StudentDeleteSemesterRequestSerializer,
    UnitSelectionRequestSerializer,
    AddRemoveRequestSerializer,
)
from education.models import SemesterCourse, StudentCourse, Semester, Course
from .models import (
    SemesterRegistrationRequest,
    RevisionRequest,
    AddRemoveRequest,
    EmergencyRemovalRequest,
    StudentDeleteSemesterRequest,
    EmploymentEducationRequest,
    UnitSelectionRequest
)
from .filters import (
    CorseFilter,
    SemesterCourseFilter,
    StudentCourseFilter,
    StudentExamFilter
)
from .pagination import DefaultPagination
from .versioning import DefaultVersioning
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Q


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    filterset_class = CorseFilter
    permission_classes = [IsAuthenticated, IsStudent]
    search_fields = ['course_name']
    ordering_fields = ['course_code', 'department__department_name', 'major__major_name',
                       'credit_num']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return CourseSerializer

        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        student = Student.objects.get(user = self.request.user)
        department = student.major.department
        return Course.objects.filter(availablity='A' , department = department).order_by('course_name')

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SemesterCourseViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    filterset_class = SemesterCourseFilter
    permission_classes = [IsAuthenticated, IsStudent]
    search_fields = ['course__course_name']
    ordering_fields = ['instructor__user__first_name', 'instructor__user__last_name',
                       'course_capacity', ]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return SemesterCourseSerializer

        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        last_semester = Semester.objects.order_by('-start_semester').first()
        return SemesterCourse.objects.filter(semester=last_semester)\
                .select_related('course', 'instructor')\
                .prefetch_related('class_days')\
                .order_by('course__course_name')

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class StudentCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    filterset_class = StudentCourseFilter
    permission_classes = [IsAuthenticated, IsStudent]
    search_fields = ['semester_course__course__course_name']
    ordering_fields = ['entry_semester']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return StudentCourseSerializer
        
        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        last_semester = Semester.objects.order_by('-start_semester').first()
        return StudentCourse.objects.filter(student__user=self.request.user,
                                            semester_course__semester=last_semester)\
                    .select_related('semester_course__course', 'semester_course__instructor')\
                    .prefetch_related('semester_course__class_days')\
                    .all()


class StudentPassedCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    filterset_class = StudentCourseFilter
    permission_classes = [IsAuthenticated, IsStudent]
    search_fields = ['semester_course__course__course_name']
    ordering_fields = ['entry_semester']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return StudentCourseSerializer

        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        return StudentCourse.objects.filter(
            student__user=self.request.user,
            score__isnull=False,
            score__gte=10,
        ).filter(Q(status = 'R') | Q(status = 'F')).select_related('student').all()


class StudentExamsViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    filterset_class = StudentExamFilter
    permission_classes = [IsAuthenticated, IsStudent]
    search_fields = ['semester_course__course__course_name']
    ordering_fields = ['entry_semester']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return ExamStudentCourseSerializer

        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        last_semester = Semester.objects.order_by('-start_semester').first()
        return StudentCourse.objects.filter(
            student__user=self.request.user,
            semester_course__semester=last_semester,
            status='R'
        ).select_related('student', 'semester_course__semester').all()


class StudentProfileViewset(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    versioning_class = DefaultVersioning

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return ProfileStudentSerializer

        raise NotImplementedError("Unsupported version requested")

    def get_object(self):
        return Student.objects.filter(
            user=self.request.user
        ).first()


class SemesterRegistrationRequestAPIView(viewsets.GenericViewSet ,
                                         mixins.ListModelMixin ,
                                         mixins.CreateModelMixin ,
                                         mixins.RetrieveModelMixin ,
                                         ):
    """Semester Registration Request APIView Is OK"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    permission_classes = [IsAuthenticated, IsStudent]
    search_fields = ['semester__name']
    ordering_fields = ['created_at', 'semester__name']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return SemesterRegistrationRequestSerializer

        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        return SemesterRegistrationRequest.objects.filter(
                student__user=self.request.user
                ).select_related('student').all()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

        except Http404:
            return Response(
                {'detail': 'Object Not found.'}, status=status.HTTP_404_NOT_FOUND
            )

        if instance.approval_status != 'P':
            return Response(
                {'message': 'Your request has been answered and you can not delete it.'}
                , status=status.HTTP_403_FORBIDDEN
            )

        if UnitSelectionRequest.objects.filter(
                semester_registration_request=instance
        ).first() is not None:
            return Response(
                {'message': 'You have unit selection for this request.'}
            )

        instance.delete()
        return Response(
            {'message': 'Resource deleted successfully.'}, status=status.HTTP_204_NO_CONTENT
        )

class UnitSelectionRequestAPIView(viewsets.ModelViewSet):
    """UnitSelectionRequestAPIView is OK excpt GPA """
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    permission_classes = [
        IsAuthenticated,
        IsStudent,
        # HavePermosionForUnitSelectionForLastSemester,
        # HavePermissionBasedOnUnitSelectionTime,
    ]

    ordering_fields = ['created_at', 'approval_status']
    versioning_class = DefaultVersioning

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return UnitSelectionRequestSerializer
        raise NotImplementedError("Unsupported version requested")
    
    def get_queryset(self):
        return UnitSelectionRequest.objects.filter(
                semester_registration_request__student__user=self.request.user
                ).select_related('semester_registration_request__student').all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.delete(instance)
        return Response(
            {"message": "UnitSelectionRequest deleted successfully"},
              status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')
    
class StudentDeleteSemesterRequestAPIView(mixins.CreateModelMixin,
                                          mixins.RetrieveModelMixin,
                                          mixins.DestroyModelMixin,
                                          mixins.ListModelMixin,
                                          viewsets.GenericViewSet,
                                          ):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    # permission_classes = [IsAuthenticated, IsStudent]
    ordering_fields = ['created_at', 'approval_status']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return StudentDeleteSemesterRequestSerializer
        raise NotImplementedError("Unsupported version requested")
    

    def get_queryset(self):
        return StudentDeleteSemesterRequest.objects.filter(
                semester_registration_request__student__user=self.request.user
                ).select_related('semester_registration_request__student').all()

    # def perform_create(self, serializer):
    #     serializer.save(student=self.request.user.student)


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.teacher_approval_status != 'P' or instance.educational_assistant_approval_status != 'P':
            return Response(
                {'message': 'your request has been answered and you can not delete it.'}
                , status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(
            {'message': 'Resource deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
         )


class RevisionRequestAPIView(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet,
                             ):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    permission_classes = [IsAuthenticated, IsStudent]
    ordering_fields = ['created_at']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return RevisionRequestSerializer
        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        return RevisionRequest.objects.filter(
                student__user=self.request.user
                ).select_related('student').all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.teacher_approval_status != 'P' or instance.educational_assistant_approval_status != 'P':
            return Response(
                {'message': 'your request has been answered and you can not delete it.'}
                , status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(
            {'message': 'Resource deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
         )


class EmergencyRemovalRequestAPIView(mixins.CreateModelMixin,
                                     mixins.RetrieveModelMixin,
                                     mixins.DestroyModelMixin,
                                     mixins.ListModelMixin,
                                     viewsets.GenericViewSet,
                                     ):

    """
        Send a Reuest to Your Advisor and If Accepted your course
        will be remove from your courses
    """
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    permission_classes = [IsAuthenticated, IsStudent]
    ordering_fields = ['created_at']
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return EmergencyRemovalRequestSerializer

        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        return EmergencyRemovalRequest.objects.filter(
                student__user=self.request.user
                ).select_related('student').all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.approval_status != 'P':
            return Response(
                {'message': 'your request has been answered and you can not delete it.'}
                , status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({'message': 'Resource deleted successfully.'},
                        status=status.HTTP_204_NO_CONTENT)


class EmploymentEducationRequestApiView(mixins.CreateModelMixin,
                                        mixins.RetrieveModelMixin,
                                        mixins.DestroyModelMixin,
                                        mixins.ListModelMixin,
                                        viewsets.GenericViewSet,
                                        mixins.UpdateModelMixin,
                                        ):

    """
        If Student have accept military status can Send
    """
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    permission_classes = [IsAuthenticated, IsStudent,HavePermssionEmoloymentDegreeTime]
    ordering_fields = ['created_at']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return EmploymentEducationRequestSerializer
        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        return EmploymentEducationRequest.objects.filter(
                student__user=self.request.user
                ).select_related('student').all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.approval_status != 'P':
            return Response(
                {'message': 'your request has been answered and you can not delete it.'},
                status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(
            {'message': 'Resource deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
            )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class AddRemoveRequestAPIView(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.DestroyModelMixin,
                                    mixins.ListModelMixin,
                                    viewsets.GenericViewSet,
                                    ):
    """AddRemove"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefaultVersioning
    permission_classes = [
        IsAuthenticated,
        IsStudent,
        # HavePermosionForUnitSelectionForLastSemester,
        # HavePermissionBasedOnAddAndRemoveTime,
    ]

    ordering_fields = ['created_at', 'approval_status']
    versioning_class = DefaultVersioning

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return AddRemoveRequestSerializer
        raise NotImplementedError("Unsupported version requested")
    
    def get_queryset(self):
        return AddRemoveRequest.objects.filter(
                semester_registration_request__student__user=self.request.user
                ).select_related('semester_registration_request__student').all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance.approval_status != 'P':
            return Response(
            {"message": "can not delete answered request"},
              status=status.HTTP_403_FORBIDDEN)
            
        serializer.delete(instance)
        return Response(
            {"message": "UnitSelectionRequest deleted successfully"},
              status=status.HTTP_204_NO_CONTENT)