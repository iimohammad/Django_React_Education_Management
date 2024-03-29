from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShowSemestersView,
    SemesterCourseViewSet,
)

router = DefaultRouter()
router.register('Semester-Show', ShowSemestersView, basename="SemesterShow")
router.register('my-Courses-Semester', SemesterCourseViewSet, basename='SemesterCourse')

urlpatterns = [
    path('', include(router.urls)),
]
