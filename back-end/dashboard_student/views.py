from rest_framework import viewsets , mixins
from rest_framework import generics 
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStudent
from accounts.models import Student, Teacher
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import ExamStudentCourseSerializer, ProfileStudentSerializer, \
                        SemesterCourseSerializer, SemesterRegistrationRequestSerializer , \
                        StudentCourseSerializer
from education.models import SemesterCourse , StudentCourse
from .models import SemesterRegistrationRequest , RevisionRequest , AddRemoveRequest , \
                    EnrollmentRequest , EmergencyRemovalRequest , StudentDeleteSemesterRequest , \
                    EmploymentEducationRequest
from .filters import SemesterCourseFilter , StudentCourseFilter, StudentExamFilter
from .pagination import DefaultPagination
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

# from .models import (
#     EnrollmentRequest,
# ) 
# from .serializers import (
#     EducationalAssistantEnrollmentRequestSerializer,
#     EnrollmentRequestSerializer,
#     StudentEnrollmentRequestSerializer,
# )

# class BaseUpdateFieldViewSet(viewsets.ReadOnlyModelViewSet):
#     allowed_fields = set()

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
        
#         for field in request.data.keys():
#             if field not in self.allowed_fields:
#                 return Response({'error': f'Updating {field} is not allowed'}, status=status.HTTP_403_FORBIDDEN)

#         self.perform_update(serializer)
#         return Response(serializer.data)
# class EnrollmentRequestViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated, IsEducationalAssistant | IsStudent | IsAdminUser]

#     def get_queryset(self):
#         return EnrollmentRequest.objects.all()

#     def get_serializer_class(self):
#         user = self.request.user
#         if hasattr(user, 'educationalassistant'):
#             return EducationalAssistantEnrollmentRequestSerializer
#         elif hasattr(user, 'student'):
#             return StudentEnrollmentRequestSerializer
#         else:
#             return EnrollmentRequestSerializer

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         approval_status = request.data.get('approval_status')
        
#         if approval_status in ['A', 'R']:
#             if instance.approval_status != 'P':
#                 return Response({'error': 'This request has already been processed'}, status=status.HTTP_400_BAD_REQUEST)

#             instance.approval_status = approval_status
#             instance.save()
#             return Response({'message': 'Enrollment request updated successfully'})

#         return Response({'error': 'Invalid approval status'}, status=status.HTTP_400_BAD_REQUEST)


class SemesterCourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SemesterCourse.objects.all()
    serializer_class = SemesterCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SemesterCourseFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated,IsStudent]
    search_fields = ['course__course_name']
    ordering_fields = ['class_days','instructor__user__first_name','instructor__user__last_name',
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
    
class StudentProfileViewset(generics.RetrieveAPIView):
    serializer_class = ProfileStudentSerializer
    permission_classes = [IsAuthenticated,IsStudent]
    def get_object(self):
        return Student.objects.filter(user = self.request.user).first()

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
        return SemesterRegistrationRequest.objects.filter \
                            (student__user = self.request.user).all()
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
        except Http404:
            return Http404()
        if instance.educational_assistant_visited or instance.teacher_visited :
            return Response({'message': 'your request has been visited and you can not delete it.'},status=status.HTTP_204_NO_CONTENT)
        self.perform_destroy(instance)
        return instance