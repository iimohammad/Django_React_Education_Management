from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet
router = DefaultRouter()

router.register("teacher", TeacherViewSet, basename="teacher")

urlpatterns = [
    path('', include(router.urls)),
]