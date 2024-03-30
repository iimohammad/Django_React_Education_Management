from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import UserProfileImageViewSet

from .views import  SemesterCourseViewSet, ShowSemestersView
from . import views
router = DefaultRouter()
router.register('Semester-Show', ShowSemestersView, basename="SemesterShow")
router.register('my-Courses-Semester', SemesterCourseViewSet,
                basename='SemesterCourse')

urlpatterns = [
    path('', include(router.urls)),
    path('show-profile/', views.show_profile, name='show_profile'),
    path('update-profile/',views.update_profile,name = 'update_profile')

]
