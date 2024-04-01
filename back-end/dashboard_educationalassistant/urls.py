from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import StudentApiView, StudentViewSet, TeacherViewSet, EducationalAssistantChangeProfileView, EducationAssistantApprovedViewSet, AcceptedStudentCourses, StudentCoursesInProgress
router = DefaultRouter()

router.register("students", StudentViewSet, basename="students")
router.register("teachers", TeacherViewSet, basename="teachers")

urlpatterns = [
    path('', include(router.urls)),
    path('students/<int:pk>/', StudentApiView.as_view(), name='student_detail'),
    path('EditProfile/', EducationalAssistantChangeProfileView.as_view(), name= 'AssistantProfile'),
    path('student/<int:student_id>/pass-courses-report/', AcceptedStudentCourses.as_view()),
    path('student/<int:student_id>/term-courses/', StudentCoursesInProgress.as_view()),
    path('assistant/<int:assistant_id>/courses/<int:course_id>/prof-approved/'),
    path('assistant/<int:assistant_id>/courses/<int:course_id>/prof-approved/{pk}/'),
    path('assistant/<int:assistant_id>/courses/<int:course_id>/prof-approved/{pk}/')
]