from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SemesterCourseViewSet, ShowSemestersView

router = DefaultRouter()
router.register('Semester-Show', ShowSemestersView, basename="SemesterShow")
router.register('my-Courses-Semester', SemesterCourseViewSet,
                basename='SemesterCourse')

urlpatterns = [
    path('', include(router.urls)),
]
