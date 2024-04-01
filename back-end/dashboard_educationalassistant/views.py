from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Student, Teacher, EducationalAssistant
from education.models import Course, SemesterCourse, Major
from dashboard_student.models import EmergencyRemovalRequest, StudentDeleteSemesterRequest, EmploymentEducationRequest

from .filters import (
                        StudentFilter,
                        TeacherFilter,
                        CourseFilter,
                        SemesterCourseFilter,
                        EmergencyRemovalRequestFilter,
                        StudentDeleteSemesterRequestFilter,
                        EmploymentEducationRequestFilter,
                     )
from .pagination import DefaultPagination
from .permissions import IsEducationalAssistant
from .serializers import (
                            StudentSerializer,
                            TeacherSerializer,
                            CourseSerializer,
                            SemesterCourseSerializer,
                            EmergencyRemovalRequestSerializer,
                            StudentDeleteSemesterRequestSerializer,
                            EmploymentEducationRequestSerializer,
                         )


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


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    search_fields = ['course_name', 'course_code']
    ordering_fields = ['course_code']

    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = Course.objects.filter(
            department=educational_assistant.field.department,
            major=educational_assistant.field
        )

        return queryset
    
    def create(self, request, *args, **kwargs):
        educational_assistant = request.user.educationalassistant
        semester_data = request.data
        major_id = semester_data.get('major')

        try:
            major = Major.objects.get(id=major_id)
            if major.department == educational_assistant.field.department and \
                    major == educational_assistant.field:
                serializer = self.get_serializer(data=semester_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail':
                    'You can only create courses relevant to your department and major.'},
                                status=status.HTTP_403_FORBIDDEN)
        except Major.DoesNotExist:
            return Response({'detail': 'Invalid major ID provided.'}, status=status.HTTP_400_BAD_REQUEST)


class SemesterCourseViewSet(viewsets.ModelViewSet):
    serializer_class = SemesterCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SemesterCourseFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    search_fields = ['exam_location']
    ordering_fields = ['exam_datetime', 'course_capacity']

    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = SemesterCourse.objects.filter(
            course__department=educational_assistant.field.department,
            course__major=educational_assistant.field
        )

        return queryset
    
    def create(self, request, *args, **kwargs):
        educational_assistant = request.user.educationalassistant
        semester_data = request.data
        course_id = semester_data.get('course')

        try:
            course = Course.objects.get(id=course_id)
            if course.department == educational_assistant.field.department and \
                    course.major == educational_assistant.field:
                serializer = self.get_serializer(data=semester_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail':
                    'You can only create semester courses relevant to your department and major.'},
                                status=status.HTTP_403_FORBIDDEN)
        except Course.DoesNotExist:
            return Response({'detail': 'Invalid course ID provided.'}, status=status.HTTP_400_BAD_REQUEST)


class EmergencyRemovalRequestViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencyRemovalRequestSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EmergencyRemovalRequestFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    ordering_fields = ['created_at']

    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = EmergencyRemovalRequest.objects.filter(
            approval_status = 'P',
            student__major=educational_assistant.field
        )

        return queryset

    def update(self, request, *args, **kwargs):
        """
        Custom update method that executes after a successful PUT request.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        # Perform additional actions here (e.g., send notifications, log changes, etc.)
        # ...

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Disallow POST requests.
        """
        return Response({"detail": "POST requests are not allowed."}, status=405)

    def destroy(self, request, *args, **kwargs):
        """
        Disallow DELETE requests.
        """
        return Response({"detail": "DELETE requests are not allowed."}, status=405)


class StudentDeleteSemesterRequestViewSet(viewsets.ModelViewSet):
    serializer_class = StudentDeleteSemesterRequestSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = StudentDeleteSemesterRequestFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    ordering_fields = ['created_at']

    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = StudentDeleteSemesterRequest.objects.filter(
            teacher_approval_status = 'A',
            educational_assistant_approval_status = 'P',
            semester_registration_request__student__major=educational_assistant.field
        )

        return queryset

    def update(self, request, *args, **kwargs):
        """
        Custom update method that executes after a successful PUT request.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        # Perform additional actions here (e.g., send notifications, log changes, etc.)
        # ...

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Disallow POST requests.
        """
        return Response({"detail": "POST requests are not allowed."}, status=405)

    def destroy(self, request, *args, **kwargs):
        """
        Disallow DELETE requests.
        """
        return Response({"detail": "DELETE requests are not allowed."}, status=405)


class EmploymentEducationRequestViewSet(viewsets.ModelViewSet):
    serializer_class = EmploymentEducationRequestSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EmploymentEducationRequestFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    ordering_fields = ['created_at']

    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = EmploymentEducationRequest.objects.filter(
            approval_status = 'P',
            student__major = educational_assistant.field
        )

        return queryset

    def update(self, request, *args, **kwargs):
        """
        Custom update method that executes after a successful PUT request.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        # Perform additional actions here (e.g., send notifications, log changes, etc.)
        # ...

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Disallow POST requests.
        """
        return Response({"detail": "POST requests are not allowed."}, status=405)

    def destroy(self, request, *args, **kwargs):
        """
        Disallow DELETE requests.
        """
        return Response({"detail": "DELETE requests are not allowed."}, status=405)
