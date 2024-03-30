import csv
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Teacher, User
from accounts.permissions import IsTeacher
from education.models import Course, Semester, SemesterCourse, StudentCourse
from education.serializers import StudentCourseSerializer
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from accounts.serializers import EditTeacherProfileSerializers, TeacherSerializer, UserProfileImageSerializer

# Show Semesters with Details
class ShowSemestersView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = ShowSemestersSerializers
    queryset = Semester.objects.all()

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


class SemesterCourseViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = SemesterCourseSerializer

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



@api_view(['GET'])
@permission_classes([IsAuthenticated,IsTeacher])
def show_profile(request):
    user = request.user
    
    try:
        # Get the teacher instance associated with the current user
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        # Handle the case where the user is not a teacher
        return Response({'error': 'User is not a teacher'}, status=404)
    
    # Serialize the teacher instance
    serializer = TeacherSerializer(teacher)
    
    # Return the serialized data in the API response
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsTeacher])
def update_profile(request):
    user = request.user
    
    try:
        # Get the teacher instance associated with the current user
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        # Handle the case where the user is not a teacher
        return Response({'error': 'User is not a teacher'}, status=404)
    
    # Update the teacher instance with the request data
    serializer = TeacherSerializer(teacher, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)