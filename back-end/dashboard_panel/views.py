from django.shortcuts import render
from rest_framework import viewsets
from accounts.models import Teacher, EducationalAssistant
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import TeacherSerializers, EducationalAssistantSerializers
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = TeacherSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EducationalAssistantViewSet(viewsets.ModelViewSet):
    queryset = EducationalAssistant.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = EducationalAssistantSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    