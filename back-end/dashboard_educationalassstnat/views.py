from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *
import requests
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

class ApprovedCourseList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Create a new approved course",
        request=ApprovedCourseSerializer,
        responses={201: ApprovedCourseSerializer()}
    )
    def Create(self, request, format=None):
        serializer = ApprovedCourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description="Update an approved course",
        request=ApprovedCourseSerializer,
        responses={200: ApprovedCourseSerializer()}
    )
    def Update (self, request, pk, format=None):
        try:
            course = ApprovedCourse.objects.get(pk=pk)
        except ApprovedCourse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ApprovedCourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Delete an approved course",
        responses={204: "No Content"}
    )
    def delete(self, request, pk, format=None):
        try:
            course = ApprovedCourse.objects.get(pk=pk)
        except ApprovedCourse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SemesterCourseList(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        description="Create a new semester course",
        request=SemesterCourseSerializer,
        responses={201: SemesterCourseSerializer()}
    )
    def Create(self, request, format=None):
        serializer = SemesterCourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description="Update an semester course",
        request=ApprovedCourseSerializer,
        responses={200: ApprovedCourseSerializer()}
    )
    def Update (self, request, pk, format=None):
        try:
            course = ApprovedCourse.objects.get(pk=pk)
        except ApprovedCourse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ApprovedCourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Delete an semester course",
        responses={204: "No Content"}
    )

    def delete(self, request, pk, format=None):
        try:
            course = ApprovedCourse.objects.get(pk=pk)
        except ApprovedCourse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EducationAssistantCreate(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Create a new education assistant",
        request=EducationAssistantSerializer,
        responses={201: EducationAssistantSerializer()}
    )
    def Create (self, request,pk, format=None):
        if not request.user.is_education_deputy:
            return Response({"message": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            assistant = EducationAssistant.objects.get(pk=pk)
        except EducationAssistant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EducationAssistantSerializer(assistant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
