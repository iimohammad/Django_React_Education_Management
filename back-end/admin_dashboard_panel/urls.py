from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (SemesterViewSet,
                    EducationalAssistantViewSet,
                    StudentViewSet,
                    DepartmentViewSet,
                     TeacherViewSet,
                     CourseViewSet,
                     SemesterCourseViewSet,
                    )
router = DefaultRouter()

router.register("teacher", TeacherViewSet, basename="teacher")
router.register('EducationalAssist',EducationalAssistantViewSet,basename="EducationalAssistant")
router.register('Student',StudentViewSet,basename="Student")
router.register('Department',DepartmentViewSet,basename="Department")
router.register('Semester',SemesterViewSet,basename="Semester")
router.register('Course',CourseViewSet,basename="Course")
router.register('SemesterCourse',SemesterCourseViewSet,basename="SemesterCourse")

urlpatterns = [
    path('', include(router.urls)),
]