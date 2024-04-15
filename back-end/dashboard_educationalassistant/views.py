from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, viewsets, status, views , mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date
from .tasks import (
    send_revision_request_approval_email,
    send_revision_request_rejection_email,
    send_semester_deletion_approval_email,
    send_semester_deletion_rejection_email,
)

from accounts.models import Student, Teacher, EducationalAssistant, User
from education.models import Course, SemesterCourse, Major, Semester
from dashboard_student.models import (EmergencyRemovalRequest,
                                      StudentDeleteSemesterRequest,
                                      EmploymentEducationRequest,
                                      RevisionRequest)


from accounts.models import Student, Teacher, EducationalAssistant
from education.models import Course, SemesterCourse, Major, StudentCourse
from dashboard_student.models import (EmergencyRemovalRequest,
                                      StudentDeleteSemesterRequest,
                                      EmploymentEducationRequest)

from .filters import (
    StudentFilter,
    TeacherFilter,
    CourseFilter,
    SemesterCourseFilter,
    EmergencyRemovalRequestFilter,
    StudentDeleteSemesterRequestFilter,
    EmploymentEducationRequestFilter,
    RevisionRequestFilter,
    StudentCourseFilter,
)
from .pagination import DefaultPagination
from .permissions import IsEducationalAssistant
from .serializers import (StudentSerializer,
                          TeacherSerializer,
                          EducationalAssistantSerializer,
                          StudentCourseSerializer)
from rest_framework.response import Response
from rest_framework import status


from .serializers import (
    StudentSerializer,
    TeacherSerializer,
    CourseSerializer,
    SemesterCourseSerializer,
    EmergencyRemovalRequestSerializer,
    StudentDeleteSemesterRequestSerializer,
    EmploymentEducationRequestSerializer,
    UserSerializer,
    RevisionRequestSerializer,
)

from .versioning import DefualtVersioning


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    search_fields = ['user__username', 'user__first_name', 'user__last_name',
                     'user__national_code',
                     ]
    ordering_fields = ['entry_semester']
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return StudentSerializer
    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = Student.objects.filter(
            major=educational_assistant.field
        )

        return queryset


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TeacherFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    search_fields = ['title', 'description']
    ordering_fields = ['entry_semester']
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return TeacherSerializer
    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = Teacher.objects.filter(
            department=educational_assistant.field.department
        )
        return queryset


class ShowProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return EducationalAssistantSerializer
    def get_object(self):
        user = self.request.user

        try:
            educational_assistant = EducationalAssistant.objects.get(user=user)

            return educational_assistant
        except Teacher.DoesNotExist:

            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'error': 'User is not an educational assistant'}, status=404)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class EducationalAssistantProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return UserSerializer
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# class EducationalAssistantChangeProfileView(generics.RetrieveUpdateAPIView):
#     queryset = EducationalAssistant.objects.all()
#     permission_classes = [IsAuthenticated, IsEducationalAssistant]
#     versioning_class = DefualtVersioning
    
#     def get_serializer_class(self, *args, **kwargs):
#         if self.request.version == 'v1':
#             return EducationalAssistantSerializer
#     def get_object(self):
#         return self.request.user.educationalassistant


class StudentPassedCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    filterset_class = StudentCourseFilter
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    search_fields = ['semester_course__course__course_name']
    ordering_fields = ['score']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return StudentCourseSerializer

        raise NotImplementedError(_("Unsupported version requested"))

    def get_queryset(self):
        major = self.request.user.educationalassistant.field
        return StudentCourse.objects.filter(
            student__major=major,
            score__isnull=False,
            status='F',
            )
    
    def retrieve(self, request, pk, format=None):
        try:
            major = self.request.user.educationalassistant.field
            passed_courses = StudentCourse.objects.filter(
                student__id=pk,
                score__isnull=False,
                student__major=major,
                status=StudentCourse.FINALREGISTERED
            )
            if not passed_courses.exists():
                raise StudentCourse.DoesNotExist("Student not found or no passed courses.")

            serializer = StudentCourseSerializer(passed_courses, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentCourse.DoesNotExist as e:

            return Response(
                {"detail": f"{str(e)}"},
                status=status.HTTP_404_NOT_FOUND,
            )


class StudentRegisteredCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    filterset_class = StudentCourseFilter
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    search_fields = ['semester_course__course__course_name']
    ordering_fields = ['score']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return StudentCourseSerializer

        raise NotImplementedError(_("Unsupported version requested"))

    def get_queryset(self):
        last_semester = Semester.objects.order_by('-start_semester').first()
        major = self.request.user.educationalassistant.field
        return StudentCourse.objects.filter(
            student__major=major,
            status='R',
            semester_course__semester=last_semester,
            )
    
    # def retrieve(self, request, pk, format=None):
    #     try:
    #         today = date.today()
    #         major = self.request.user.educationalassistant.field
    #         registered_courses = StudentCourse.objects.filter(
    #             student__id=pk,
    #             score__isnull=True,
    #             student__major=major,
    #             status=StudentCourse.REGISTERED,
    #             semester_course__semester__start_semester__lte=today,
    #             semester_course__semester__end_semester__gte=today
    #         )
    #         if not registered_courses.exists():
    #             raise StudentCourse.DoesNotExist("Student not found or no registered courses.")

    #         serializer = StudentCourseSerializer(registered_courses, many=True)

    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except StudentCourse.DoesNotExist as e:

    #         return Response(
    #             {"detail": f"{str(e)}"},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )


class CourseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    search_fields = ['course_name', 'course_code']
    ordering_fields = ['course_code']
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return CourseSerializer
    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = Course.objects.filter(
            department=educational_assistant.field.department,
            # major=educational_assistant.field
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
        
    def update(self, request, *args, **kwargs):
        course_instance = self.get_object()
        educational_assistant = request.user.educationalassistant
        semester_data = request.data
        major_id = semester_data.get('major')

        try:
            major = Major.objects.get(id=major_id)
            if major.department == educational_assistant.field.department and \
                    major == educational_assistant.field:
                serializer = self.get_serializer(instance=course_instance,
                                                 data=semester_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail':
                                     'You can only update courses relevant to your department and major.'},
                                status=status.HTTP_403_FORBIDDEN)
        except Major.DoesNotExist:
            return Response({'detail': 'Invalid major ID provided.'}, status=status.HTTP_400_BAD_REQUEST)


class SemesterCourseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SemesterCourseFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    search_fields = ['exam_location']
    ordering_fields = ['exam_datetime', 'course_capacity']
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return SemesterCourseSerializer
    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = SemesterCourse.objects.filter(
            course__department=educational_assistant.field.department,
            # course__major=educational_assistant.field
        )

        return queryset

    def create(self, request, *args, **kwargs):
        educational_assistant = request.user.educationalassistant
        semester_course_data = request.data
        course_id = semester_course_data.get('course')
        semester_id = semester_course_data.get('semester')

        try:
            course = Course.objects.get(id=course_id)
            semester = Semester.objects.get(id=semester_id)
            try:
                semester_addremove_end = semester.addremove.addremove_end
                if semester_addremove_end == None:
                    raise Exception("This semester has no addremove date data!")
            except Exception as e:
                return Response({'detail': f"{str(e)}"},
                                status=status.HTTP_404_NOT_FOUND)
            today = date.today()

            if course.department == educational_assistant.field.department and \
                    course.major == educational_assistant.field:
                if today <= semester_addremove_end:
                    if course.course_type == 'A' or course.course_type == 'I' or course.course_type == 'L':
                        semester_course_data["exam_datetime"] = None
                        semester_course_data["exam_location"] = None
                    if course.availablity == 'D':
                        return Response({'detail':
                                "This course is deleted! Please select another course."},
                                        status=status.HTTP_403_FORBIDDEN)
                    serializer = self.get_serializer(data=semester_course_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'detail':
                            "It's past add and remove time range. Please try again for the next semester!"},
                                status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'detail':
                            'You can only create semester courses relevant to your department and major.'},
                        status=status.HTTP_403_FORBIDDEN)

        except Course.DoesNotExist:
            return Response({'detail': 'Invalid course ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        except Semester.DoesNotExist:
            return Response({'detail': 'Invalid semester ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        semester_course_instance = self.get_object()
        educational_assistant = request.user.educationalassistant
        semester_course_data = request.data
        course_id = semester_course_data.get('course')
        semester_id = semester_course_data.get('semester')

        try:
            course = Course.objects.get(id=course_id)
            semester = Semester.objects.get(id=semester_id)
            try:
                semester_addremove_end = semester.addremove.addremove_end
                if semester_addremove_end == None:
                    raise SemesterCourse.DoesNotExist("This semester has no addremove date data!")
            except SemesterCourse.DoesNotExist as e:
                return Response({'detail': f"{str(e)}"},
                                status=status.HTTP_404_NOT_FOUND)
            today = date.today()

            if course.department == educational_assistant.field.department and \
                    course.major == educational_assistant.field:
                if today <= semester_addremove_end:
                    if course.course_type == 'A' or course.course_type == 'I' or course.course_type == 'L':
                        semester_course_data["exam_datetime"] = None
                        semester_course_data["exam_location"] = None
                    if course.availablity == 'D':
                        return Response({'detail':
                                "You cannot update the semester course's availability here!"},
                                        status=status.HTTP_403_FORBIDDEN)
                    serializer = self.get_serializer(instance=semester_course_instance,
                                                     data=semester_course_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'detail':
                            "It's past add and remove time range. Please try again for the next semester!"},
                                status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'detail':
                            'You can only create semester courses relevant to your department and major.'},
                        status=status.HTTP_403_FORBIDDEN)

        except Course.DoesNotExist:
            return Response({'detail': 'Invalid course ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        except Semester.DoesNotExist:
            return Response({'detail': 'Invalid semester ID provided.'}, status=status.HTTP_400_BAD_REQUEST)


class EmergencyRemovalRequestViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EmergencyRemovalRequestFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    ordering_fields = ['created_at']
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return EmergencyRemovalRequestSerializer

    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = EmergencyRemovalRequest.objects.filter(
            approval_status='P',
            student__major=educational_assistant.field
        )

        return queryset

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


class StudentDeleteSemesterRequestViewSet(viewsets.GenericViewSet ,
                                          mixins.ListModelMixin ,
                                          mixins.RetrieveModelMixin ,
                                          mixins.UpdateModelMixin ,
                                          ):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = StudentDeleteSemesterRequestFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    ordering_fields = ['created_at']
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return StudentDeleteSemesterRequestSerializer

    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = StudentDeleteSemesterRequest.objects.filter(
            teacher_approval_status='A',
            educational_assistant_approval_status='P',
            semester_registration_request__student__major=educational_assistant.field
        )
        return queryset


class EmploymentEducationRequestViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EmploymentEducationRequestFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    ordering_fields = ['created_at']
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return EmploymentEducationRequestSerializer
    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant

        queryset = EmploymentEducationRequest.objects.filter(
            approval_status='P',
            student__major=educational_assistant.field
        )

        return queryset

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


class RevisionRequestViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RevisionRequestFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsEducationalAssistant]
    ordering_fields = ['created_at']
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return RevisionRequestSerializer
    def get_queryset(self):
        educational_assistant = self.request.user.educationalassistant
        today = date.today()

        queryset = RevisionRequest.objects.filter(
            teacher_approval_status='A',
            educational_assistant_approval_status='P',
            student__major=educational_assistant.field,
            # course__semester_course__semester__start_semester__lte=today,
            # course__semester_course__semester__end_semester__gte=today
        )

        return queryset

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