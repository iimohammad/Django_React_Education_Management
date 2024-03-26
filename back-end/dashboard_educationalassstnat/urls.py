from rest_framework.routers import DefaultRouter
from .views import ApprovedCourseList, SemesterCourseList , EducationAssistantCreate
from django.urls import path, include

router = DefaultRouter()  

router.register('ApprovedCourse', ApprovedCourseList, basename='ApprovedCourse') 
router.register('SemesterCourse',SemesterCourseList,basename='SemesterCourse')
router.register('EducationAssistant',EducationAssistantCreate,basename='EducationAssistant')


urlpatterns = [
    path('', include(router.urls)),  
]