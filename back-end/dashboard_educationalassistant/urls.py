from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import StudentApiView, StudentViewSet, TeacherViewSet, CourseViewSet, SemesterCourseViewSet

router = DefaultRouter()

router.register("students", StudentViewSet, basename="students")
router.register("teachers", TeacherViewSet, basename="teachers")
router.register("courses", CourseViewSet, basename="courses")
router.register("semester_courses", SemesterCourseViewSet, basename="semester_courses")

urlpatterns = [
    path('', include(router.urls)),
    path('students/<int:pk>/', StudentApiView.as_view(), name='student_detail')
]
