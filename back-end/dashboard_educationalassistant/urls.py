from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet , TeacherViewSet , StudentApiView

router = DefaultRouter()

router.register("students", StudentViewSet, basename="students")
router.register("teachers", TeacherViewSet, basename="teachers")

urlpatterns = [
    path('', include(router.urls)),
    path('students/<int:pk>/' ,StudentApiView.as_view() , name='student_detail')
]