from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import IsEducationalAssistant,IsStudent
from accounts.models import Student, Teacher
from accounts.serializers import StudentSerializer, TeacherSerializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import SemesterCourseSerializer , StudentCourseSerializer
from education.models import SemesterCourse , StudentCourse
from .filters import SemesterCourseFilter , StudentCourseFilter
from .pagination import DefaultPagination
from .models import (
    EnrollmentRequest,
) 
from .serializers import (
    EducationalAssistantEnrollmentRequestSerializer,
    EnrollmentRequestSerializer,
    StudentEnrollmentRequestSerializer,
)

class BaseUpdateFieldViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_fields = set()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        for field in request.data.keys():
            if field not in self.allowed_fields:
                return Response({'error': f'Updating {field} is not allowed'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_update(serializer)
        return Response(serializer.data)

class StudentViewSet(BaseUpdateFieldViewSet):
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    allowed_fields = { 'advisor', 'military_service_status'}

class TeacherViewSet(BaseUpdateFieldViewSet):
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializers
    allowed_fields = {'expertise', 'rank'}

class EnrollmentRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsEducationalAssistant | IsStudent | IsAdminUser]

    def get_queryset(self):
        return EnrollmentRequest.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if hasattr(user, 'educationalassistant'):
            return EducationalAssistantEnrollmentRequestSerializer
        elif hasattr(user, 'student'):
            return StudentEnrollmentRequestSerializer
        else:
            return EnrollmentRequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        approval_status = request.data.get('approval_status')
        
        if approval_status in ['A', 'R']:
            if instance.approval_status != 'P':
                return Response({'error': 'This request has already been processed'}, status=status.HTTP_400_BAD_REQUEST)

            instance.approval_status = approval_status
            instance.save()
            return Response({'message': 'Enrollment request updated successfully'})

        return Response({'error': 'Invalid approval status'}, status=status.HTTP_400_BAD_REQUEST)


class SemesterCourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SemesterCourse.objects.all()
    serializer_class = SemesterCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SemesterCourseFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated,IsStudent]
    search_fields = ['title', 'description']
    ordering_fields = ['entry_semester']

class StudentCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentCourseFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated,IsStudent]
    search_fields = ['title', 'description']
    ordering_fields = ['entry_semester']