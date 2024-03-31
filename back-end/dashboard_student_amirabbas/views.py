from rest_framework import viewsets , mixins
from rest_framework import generics 
from rest_framework.exceptions import PermissionDenied , NotFound
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStudent
from accounts.models import Student, Teacher
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import ExamStudentCourseSerializer, SemesterCourseSerializer,\
                        SemesterRegistrationRequestSerializer ,StudentCourseSerializer,\
                        UniversityAddRemoveRequestSerializerSerializer
                                                
from education.models import SemesterCourse , StudentCourse
from .models import SemesterRegistrationRequest , RevisionRequest , AddRemoveRequest , \
                    EnrollmentRequest , EmergencyRemovalRequest , StudentDeleteSemesterRequest , \
                    EmploymentEducationRequest, UnitSelectionRequest

from .filters import SemesterCourseFilter , StudentCourseFilter, StudentExamFilter
from .pagination import DefaultPagination
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


class SemesterCourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SemesterCourse.objects.all()
    serializer_class = SemesterCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SemesterCourseFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated,IsStudent]
    search_fields = ['course__course_name']
    ordering_fields = ['instructor__user__first_name','instructor__user__last_name',
                        'course_capacity',]
    
class StudentCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudentCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentCourseFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated,IsStudent]
    search_fields = ['semester_course__course__course_name']
    ordering_fields = ['entry_semester']
    def get_queryset(self):
        return StudentCourse.objects.filter(student__user =self.request.user).all()
    
class StudentExamsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExamStudentCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentExamFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated,IsStudent]
    search_fields = ['semester_course__course__course_name']
    ordering_fields = ['entry_semester']
    def get_queryset(self):
        return StudentCourse.objects.filter(student__user =self.request.user).all()
    

class SemesterRegistrationRequestAPIView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = SemesterRegistrationRequestSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated,IsStudent]
    search_fields = ['semester__name']
    ordering_fields = ['created_at' , 'semester__name']
    def get_queryset(self):
        return SemesterRegistrationRequest.objects.filter(student__user = self.request.user).all()
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
        except Http404:
            raise NotFound()
        if instance.approval_status != 'P' :
            return Response(
                {'message': 'your request has been answered and you can not delete it.'}
                , status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({'message': 'Resource deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
class UniversityAddRemoveRequestAPIView(mixins.CreateModelMixin,
                                       mixins.DestroyModelMixin,
                                       viewsets.GenericViewSet):
    serializer_class = SemesterRegistrationRequestSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated,IsStudent]
    search_fields = ['created_at']  
    ordering_fields = ['created_at', 'approval_status']

    def get_queryset(self):
        return UniversityAddRemoveRequestSerializerSerializer.objects.filter(student__user=self.request.user)

    def perform_create(self, serializer):

        # بررسی اجازه انجام درخواست بر اساس نکات ارائه شده
        semester = serializer.validated_data.get('semester')
        added_universities = serializer.validated_data.get('added_universities', [])
        removed_universities = serializer.validated_data.get('removed_universities', [])

        # بررسی تسویه مالی
        if semester.start_date < timezone.now().date():
            raise PermissionDenied("Financial clearance must be completed before add/remove")

        # بررسی انجام درخواست بعد از انتخاب واحد
        if semester.unit_selection_end > timezone.now().date():
            raise PermissionDenied("Add/remove must be done after unit selection")

        # بررسی سقف واحدهای اضافه/حذف
        total_units = sum(course.units for course in added_universities)
        if total_units > 6:
            raise PermissionDenied("Maximum 6 units can be added")

        # بررسی بازه زمانی مورد نظر
        if not (semester.start_date < timezone.now().date() < semester.end_date):
            raise PermissionDenied("The request should be made within the specified time frame")

        # ایجاد درخواست
        serializer.save(student=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            raise NotFound()

        if instance.approval_status != 'P':
            return Response({'message': 'Your request has been answered and you cannot delete it.'},
                            status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({'message': 'Resource deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)