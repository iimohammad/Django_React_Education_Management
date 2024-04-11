import csv
from django.shortcuts import get_object_or_404
from rest_framework import viewsets , mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Student, Teacher, User
from .pagination import DefaultPagination
from .versioning import DefualtVersioning
from .permissions import IsTeacher , IsAdvisor
from rest_framework.exceptions import MethodNotAllowed
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
from .tasks import send_approval_email, send_approval_email_employment
from .serializers import (
    AddRemoveRequestViewSerializers,
    CSVFileSerializer,
    EmergencyRemovalConfirmationSerializers,
    EvaluationSerializers,
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
from rest_framework.views import APIView
from dashboard_student.models import (
    EmploymentEducationRequest,
    StudentDeleteSemesterRequest,
    EmergencyRemovalRequest,
    AddRemoveRequest,
    UnitSelectionRequest,
    SemesterRegistrationRequest,
)
from rest_framework import views
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework import generics

class EvaluateStudentsViewSet(viewsets.ModelViewSet):
    """OK"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = EvaluationSerializers

    def get_queryset(self):
        teacher = self.request.user.teacher
        query = StudentCourse.objects.filter(
            semester_course__instructor=teacher
        )
        return query
    
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')
    


class EvaluateStudentsAPIView(APIView):
    """OK"""
    serializer_class = CSVFileSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        if 'file' in request.FILES:
            file_obj = request.FILES['file']
            try:
                decoded_file = file_obj.read().decode('utf-8').splitlines()
                csv_data = csv.DictReader(decoded_file)

                for row in csv_data:
                    student_id = row.get('student_id')
                    score = row.get('score')

                    # Validate data before updating the model
                    if not student_id or not score:
                        return Response(
                            {'error': 'Both student_id and score are required.'},
                                         status=status.HTTP_400_BAD_REQUEST
                                         )

                    student_course = StudentCourse.objects.filter(
                        student_id=student_id
                        ).first()
                    
                    if student_course:
                        student_course.score = score
                        student_course.save()

                return Response({'message': 'Student scores updated successfully'},
                                 status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {'error': 'An error occurred while processing the CSV file'},
                      status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'No file uploaded'},
                             status=status.HTTP_400_BAD_REQUEST)


class SemesterCourseViewSet(viewsets.ReadOnlyModelViewSet):
    """Semester CourseView Set OK"""
    
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


class RevisionRequestView(viewsets.ModelViewSet):

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
            course__semester_course__instructor = teacher)
        return queryset
    
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')


class UnitSelectionRequestView(generics.UpdateAPIView):
    """Unit Selection Request View ----------Waiting for Unit Selection-------"""
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





class AddRemoveRequestView(viewsets.ModelViewSet):
    """Add Remove Confirmation View  --------Waiting for Unit Selection--------"""
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





class StudentDeleteSemesterConfirmationAPI(viewsets.ModelViewSet):

    """Student Delete Semester Confirmation API need to change database OK"""
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
            semester_registration_request__student__in=students,
            teacher_approval_status='P',
        )

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')


class EmploymentEducationConfirmationAPI(viewsets.ModelViewSet):
    """Employment Education Confirmation API OK"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning  
    permission_classes = [IsTeacher, IsAuthenticated]

    def get_queryset(self):
        # Filter students assigned to the requesting teacher
        teacher = Teacher.objects.get(user = self.request.user)
        students = Student.objects.filter(advisor=teacher)

        # Filter delete semester requests related to those students
        return EmploymentEducationRequest.objects.filter(
            student__in=students,
            approval_status='P',
        )


    def get_serializer_class(self):
        if self.request.version == 'v1':
            return EmploymentEducationConfirmationSerializer
        raise NotImplementedError("Unsupported version requested")

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the update
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        approval_status_changed = instance.approval_status != serializer.validated_data['approval_status']
        serializer.save()

        # Send approval email if the approval status changed to 'A'
        if approval_status_changed and serializer.validated_data['approval_status'] == 'A':
            send_approval_email_employment.delay(instance.student.user.email)

        return Response(serializer.data)


class EmergencyRemovalConfirmationView(viewsets.ModelViewSet):

    """Need to change course in database and not allow if course has preeuqisite OK"""
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
    

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')
    
    # Adviser Tasks APIs
class ShowMyStudentsVeiw(viewsets.ReadOnlyModelViewSet):
    """Show My Students Veiw OK"""
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

# General Tasks
class ShowProfileAPIView(RetrieveAPIView):
    """Show Profile APIView OK"""
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
    """UserProfileUpdateAPIView OK"""
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
    """ShowSemestersView OK"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    versioning_class = DefualtVersioning
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Semester.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v1':
            return ShowSemestersSerializers
        raise NotImplementedError("Unsupported version requested")
