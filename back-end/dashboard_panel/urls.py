from django.urls import path,include
from rest_framework.routers import DefaultRouter
from admin_dashboard_panel.views import CourseViewSet,SemesterCourseViewSet
from .views import (StudentViewSet,
                    TeacherViewSet,
                    EnrollmentRequestViewSet,
                    )

router = DefaultRouter()
# Educational Assistant Urls
router.register("EucationalAssistantPanel/Students", StudentViewSet, basename="Student")
router.register("EucationalAssistantPanel/Teachers", TeacherViewSet, basename="teacher")
router.register("EucationalAssistantPanel/Course", CourseViewSet, basename="Course")
router.register("EucationalAssistantPanel/SemesterCourse", SemesterCourseViewSet, basename="SemesterCourse")


# Student Urls 

router.register(r'enrollment-requests', EnrollmentRequestViewSet,basename='enrollment')


# Teachers Urls 



urlpatterns = [
    path('', include(router.urls)),
]