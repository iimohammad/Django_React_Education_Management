from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShowSemestersView,
)

router = DefaultRouter()
router.register('Semester-Show', ShowSemestersView, basename="SemesterShow")

urlpatterns = [
    path('', include(router.urls)),
]
