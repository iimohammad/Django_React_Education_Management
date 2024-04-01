from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import StudentApiView, StudentViewSet, TeacherViewSet, EducationalAssistantChangeProfileView, CoursPassAPIview, TermCoursAPIView
router = DefaultRouter()

router.register("students", StudentViewSet, basename="students")
router.register("teachers", TeacherViewSet, basename="teachers")

urlpatterns = [
    path('', include(router.urls)),
    path('students/<int:pk>/', StudentApiView.as_view(), name='student_detail'),
    path('EditProfile/', EducationalAssistantChangeProfileView.as_view(), name= 'AssistantProfile'),
    path('student/<int:student_id>/pass-courses-report/', CoursPassAPIview.as_view()),
    path('student/<int:student_id>/term-courses/', TermCoursAPIView.as_view()),
    path('assistant/{pk,me}/courses/{c-pk}/prof-approved/'),
    path('assistant/{pk,me}/courses/{c-pk}/prof-approved/{pk}/'),
    path('assistant/{pk,me}/courses/{c-pk}/prof-approved/{pk}/')
]