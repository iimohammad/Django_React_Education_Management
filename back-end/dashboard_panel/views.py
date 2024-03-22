from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEducationalAssistant
from accounts.models import Student, Teacher
from accounts.serializers import StudentSerializer, TeacherSerializers
from education.serializers import CourseSerializers
from education.models import Course


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

