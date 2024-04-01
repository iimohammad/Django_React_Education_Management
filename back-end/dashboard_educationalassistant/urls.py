from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import StudentApiView, StudentViewSet, TeacherViewSet, EducationalAssistantChangeProfileView, CoursPass, TermCours

from .views import (
    StudentApiView,
    StudentViewSet,
    TeacherViewSet,
    CourseViewSet,
    SemesterCourseViewSet,
    EmergencyRemovalRequestViewSet,
    StudentDeleteSemesterRequestViewSet,
    EmploymentEducationRequestViewSet,
    )

router = DefaultRouter()

router.register("students", StudentViewSet, basename="students")
router.register("teachers", TeacherViewSet, basename="teachers")
router.register("courses", CourseViewSet, basename="courses")
router.register("semester_courses", SemesterCourseViewSet, basename="semester_courses")
router.register("emergency_removals", EmergencyRemovalRequestViewSet, basename="emergency_removals")
router.register("semester_removals", StudentDeleteSemesterRequestViewSet, basename="semester_removals")
router.register("education_employments", EmploymentEducationRequestViewSet, basename="education_employments")

urlpatterns = [
    path('', include(router.urls)),
    path('students/<int:pk>/', StudentApiView.as_view(), name='student_detail'),
    path('EditProfile/', EducationalAssistantChangeProfileView.as_view(), name= 'AssistantProfile'),
    path('student/{pk/me}/pass-courses-report/', CoursPass.as_view()),
    path('student/{pk/me}/term-courses/', TermCours.as_view()),
    path('assistant/{pk,me}/courses/{c-pk}/prof-approved/'),
    path('assistant/{pk,me}/courses/{c-pk}/prof-approved/{pk}/'),
    path('assistant/{pk,me}/courses/{c-pk}/prof-approved/{pk}/')
]