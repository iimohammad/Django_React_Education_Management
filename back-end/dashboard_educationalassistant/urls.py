from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import StudentApiView, StudentViewSet, TeacherViewSet, CoursPass, TermCours

from .views import (
    StudentApiView,
    StudentViewSet,
    TeacherViewSet,
    CourseViewSet,
    SemesterCourseViewSet,
    EmergencyRemovalRequestViewSet,
    StudentDeleteSemesterRequestViewSet,
    EmploymentEducationRequestViewSet,
    ShowProfileAPIView,
    EducationalAssistantProfileUpdateView,
    # EducationalAssistantChangeProfileView,
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
    path('show_profile/', ShowProfileAPIView.as_view(), name= 'show_assistant_profile'),
    path('edit_profile/', EducationalAssistantProfileUpdateView.as_view(), name= 'edit_assistant_profile'),
    # path('update_profile/', EducationalAssistantChangeProfileView.as_view(), name= 'update_assistant_profile'),
    path('student/{pk/me}/pass-courses-report/', CoursPass.as_view()),
    path('student/{pk/me}/term-courses/', TermCours.as_view()),
    # path('assistant/{pk,me}/courses/{c-pk}/prof-approved/'),
    # path('assistant/{pk,me}/courses/{c-pk}/prof-approved/{pk}/'),
    # path('assistant/{pk,me}/courses/{c-pk}/prof-approved/{pk}/')
]