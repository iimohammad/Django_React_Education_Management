import csv
from rest_framework import viewsets , mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Student, Teacher, User
from .pagination import DefaultPagination
from .versioning import DefualtVersioning
from .permissions import IsTeacher , IsAdvisor
from dashboard_professors.queryset import get_student_queryset
from dashboard_student.models import (
    RevisionRequest, 
    UnitSelectionRequest,
    SemesterRegistrationRequest
    )
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from education.models import Semester, SemesterCourse, StudentCourse
from education.serializers import StudentCourseSerializer
from .tasks import send_approval_email
from .serializers import (
    AddRemoveRequestViewSerializers,
    EmergencyRemovalConfirmationSerializers,
    RevisionRequestSerializers,
    SemesterCourseSerializer,
    SemesterRegistrationConfirmationSerializers,
    ShowSemestersSerializers,
    StudentSerializer,
    UnitSelectionRequestTeacherUpdateSerializer,
    EmploymentEducationConfirmationSerializer,
    StudentDeleteSemesterRequestTeacherSerializer,
    SemesterRegistrationRequestSerializers,
)
from accounts.serializers import (
    UserProfileImageUpdateSerializer,
    TeacherSerializer,
)
from dashboard_student.models import (
    EmploymentEducationRequest,
    StudentDeleteSemesterRequest,
    EmergencyRemovalRequest,
    AddRemoveRequest,
    UnitSelectionRequest,
    SemesterRegistrationRequest,
)

from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework import generics
from rest_framework.mixins import ListModelMixin


# General Tasks
class ShowProfileAPIView(RetrieveAPIView):
    """Show Profile APIView"""
    permission_classes = [IsAuthenticated] 
    versioning_class = DefualtVersioning
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return TeacherSerializer
        
        raise NotImplementedError("Unsupported version requested")

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


class UserProfileUpdateAPIView(UpdateAPIView):
    """UserProfileUpdateAPIView"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsTeacher]
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return UserProfileImageUpdateSerializer
        raise NotImplementedError("Unsupported version requested")

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
class ShowSemestersView(viewsets.ReadOnlyModelViewSet):
    """ShowSemestersView"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Semester.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return ShowSemestersSerializers
        raise NotImplementedError("Unsupported version requested")

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
class SemesterCourseViewSet(viewsets.ReadOnlyModelViewSet):
    """Semester CourseView Set"""
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsAuthenticated, IsTeacher]
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return SemesterCourseSerializer

        raise NotImplementedError("Unsupported version requested")

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


class RevisionRequestView(viewsets.GenericViewSet,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,):

    """Revision Confirmation View"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsAuthenticated, IsTeacher]
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return RevisionRequestSerializers
        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        teacher = Teacher.objects.get(user = self.request.user)
        queryset = RevisionRequest.objects.filter(
            course__semester_course__instructor = teacher).all()
        return queryset
    

# Adviser Tasks APIs
class ShowMyStudentsVeiw(
                        generics.GenericAPIView,
                        ListModelMixin,
                        ):
    """Show My Students Veiw"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsAuthenticated, IsTeacher]
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return StudentSerializer
        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        return get_student_queryset(self.request)


class UnitSelectionRequestView(generics.UpdateAPIView):
    """Unit Selection Request View"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsTeacher, IsAuthenticated]

    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return UnitSelectionRequestTeacherUpdateSerializer
        raise NotImplementedError("Unsupported version requested")
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        teacher = Teacher.objects.get(user = self.request.user)
        return UnitSelectionRequest.objects.filter(
            semester_registration_request__student__advisor = teacher
            ).all()


class SemesterRegistrationConfirmationViewAPI(viewsets.GenericViewSet ,
                                              mixins.ListModelMixin ,
                                              mixins.RetrieveModelMixin ,
                                              mixins.UpdateModelMixin ,
                                              ):
    """Semester Registration Confirmation View API OK"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsAuthenticated , IsTeacher]
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return SemesterRegistrationRequestSerializers
        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        teacher = Teacher.objects.get(user = self.request.user)
        return SemesterRegistrationRequest.objects.filter(student__advisor = teacher).all()



class AddRemoveRequestView(generics.UpdateAPIView):
    """Add Remove Confirmation View"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsTeacher, IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return AddRemoveRequestViewSerializers
        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        # Filter students assigned to the requesting teacher
        teacher = Teacher.objects.get(user = self.request.user)
        students = Student.objects.filter(advisor=teacher)

        # Filter delete semester requests related to those students
        return AddRemoveRequest.objects.filter(
            student__in=students
        )


class EmergencyRemovalConfirmationView(viewsets.GenericViewSet ,
                                       mixins.ListModelMixin ,
                                       mixins.RetrieveModelMixin ,
                                       mixins.UpdateModelMixin ,
                                       ):

    """Need to change course in database and not allow if course has preeuqisite"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsAuthenticated , IsTeacher]
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return EmergencyRemovalConfirmationSerializers
        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        # Filter students assigned to the requesting teacher
        teacher = Teacher.objects.get(user = self.request.user)
        students = Student.objects.filter(advisor=teacher)

        # Filter delete semester requests related to those students
        return EmergencyRemovalRequest.objects.filter(
            student__in=students
        )


class StudentDeleteSemesterConfirmationAPI(viewsets.GenericViewSet ,
                                            mixins.ListModelMixin ,
                                            mixins.RetrieveModelMixin ,
                                            mixins.UpdateModelMixin ,
                                            ):

    """Student Delete Semester Confirmation API need to change database"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsAuthenticated , IsTeacher]
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return StudentDeleteSemesterRequestTeacherSerializer
        raise NotImplementedError("Unsupported version requested")

    def get_queryset(self):
        # Filter students assigned to the requesting teacher
        teacher = Teacher.objects.get(user = self.request.user)
        students = Student.objects.filter(advisor=teacher)

        # Filter delete semester requests related to those students
        return StudentDeleteSemesterRequest.objects.filter(
            semester_registration_request__student__in=students
        )



class EmploymentEducationConfirmationAPI(
    generics.UpdateAPIView,
    generics.ListAPIView,
):
    """Employment Education Confirmation API """
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsTeacher, IsAuthenticated]
    queryset = EmploymentEducationRequest.objects.filter(approval_status='P')
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return EmploymentEducationConfirmationSerializer
        raise NotImplementedError("Unsupported version requested")
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        approval_status_changed = instance.approval_status != serializer.validated_data['approval_status']
        serializer.save()

        if approval_status_changed and serializer.validated_data['approval_status'] == 'A':
            send_approval_email.delay(instance.student.user.email)
            
        return Response(serializer.data)