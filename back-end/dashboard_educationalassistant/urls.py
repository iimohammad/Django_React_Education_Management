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
    StudentPassedCoursesViewSet,
    StudentRegisteredCoursesViewSet,
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
router.register("students_passed_courses", StudentPassedCoursesViewSet, basename="students_passed_courses")
router.register("students_registered_courses", StudentRegisteredCoursesViewSet, basename="students_registered_courses")

urlpatterns = [
    path('', include(router.urls)),
    path('show_profile/', ShowProfileAPIView.as_view(), name= 'show_assistant_profile'),
    path('edit_profile/', EducationalAssistantProfileUpdateView.as_view(),
         name= 'edit_assistant_profile'),
]