from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    StudentViewSet,
    TeacherViewSet,
    CourseViewSet,
    SemesterCourseViewSet,
    EmergencyRemovalRequestViewSet,
    StudentDeleteSemesterRequestViewSet,
    EmploymentEducationRequestViewSet,
    ShowProfileAPIView,
    EducationalAssistantProfileUpdateView,
    RevisionRequestViewSet,
    StudentPassedCoursesAPIView,
    StudentsPassedCoursesAPIView,
    StudentRegisteredCoursesAPIView,
    StudentsRegisteredCoursesAPIView,
    )

router = DefaultRouter()

router.register("students", StudentViewSet, basename="students")
router.register("teachers", TeacherViewSet, basename="teachers")
router.register("courses", CourseViewSet, basename="courses")
router.register("semester_courses", SemesterCourseViewSet, basename="semester_courses")
router.register("emergency_removals", EmergencyRemovalRequestViewSet, basename="emergency_removals")
router.register("semester_removals", StudentDeleteSemesterRequestViewSet, basename="semester_removals")
router.register("education_employments", EmploymentEducationRequestViewSet,
                basename="education_employments")
router.register("revision_requests", RevisionRequestViewSet, basename="revision_requests")

urlpatterns = [
    path('', include(router.urls)),
    path('passed_courses/', StudentPassedCoursesAPIView.as_view(), name='passed_courses'),
    path('passed_courses/<int:student_id>/', StudentsPassedCoursesAPIView.as_view(),
         name='student_passed_courses'),
    path('registered_courses/', StudentRegisteredCoursesAPIView.as_view(), name='registered_courses'),
    path('registered_courses/<int:student_id>/', StudentsRegisteredCoursesAPIView.as_view(),
         name='student_registered_courses'),
    path('show_profile/', ShowProfileAPIView.as_view(), name= 'show_assistant_profile'),
    path('edit_profile/', EducationalAssistantProfileUpdateView.as_view(),
         name= 'edit_assistant_profile'),
]