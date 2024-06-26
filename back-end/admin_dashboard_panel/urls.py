from django.urls import include, path
from rest_framework.routers import DefaultRouter
from accounts.permissions import IsAdmin

from .views import (CourseViewSet, DepartmentViewSet,
                    EducationalAssistantViewSet, SemesterCourseViewSet,
                    SemesterViewSet, StudentViewSet, TeacherViewSet,
                    )

app_name = 'dashboard_admin'
router = DefaultRouter()
# router.register("User", UserViewSet, basename="User")
router.register("teacher", TeacherViewSet, basename="teacher")
router.register('EducationalAssist', EducationalAssistantViewSet,
                basename="EducationalAssistant")
router.register('Student', StudentViewSet, basename="Student")
router.register('Department', DepartmentViewSet, basename="Department")
router.register('Semester', SemesterViewSet, basename="Semester")
router.register('Course', CourseViewSet, basename="Course")
router.register('SemesterCourse', SemesterCourseViewSet,
                basename="SemesterCourse")

urlpatterns = [
    path('', include(router.urls), name='dashboard_root'),
]
