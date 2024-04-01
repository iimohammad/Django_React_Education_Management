import csv
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Student, Teacher, User
from accounts.permissions import IsTeacher
from education.models import Semester, SemesterCourse, StudentCourse
from education.serializers import StudentCourseSerializer
from .serializers import *
from accounts.serializers import StudentSerializer, UserProfileImageUpdateSerializer, TeacherSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework import generics
from rest_framework.mixins import ListModelMixin


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


class ShowProfileAPIView(RetrieveAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]  # Assuming IsTeacher permission is checked inside serializer

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


class UserProfileImageView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileImageUpdateSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ShowMyStudentsVeiw(generics.GenericAPIView, ListModelMixin):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        if isinstance(self.request.user, User):
            user_id = self.request.user
        else:
            user_id = self.request.user.id

        return Student.objects.filter(advisor__user=user_id)


class UnitSelectionRequestShows(generics.ListCreateAPIView):
    # serializer_class = 
    pass
    # @action(name="Accept")
    # @action(name = "Reject")
