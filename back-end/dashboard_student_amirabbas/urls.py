from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import SemesterCourseViewSet , StudentCoursesViewSet, \
                    StudentExamsViewSet, SemesterRegistrationRequestAPIView
                    
                    

router = DefaultRouter()


router.register('semester_courses' , SemesterCourseViewSet , basename='semestercourse')
router.register('student_courses' , StudentCoursesViewSet , basename='studentcourses')
router.register('student_exams' , StudentExamsViewSet , basename='studentexams')
router.register('semester_registration' , SemesterRegistrationRequestAPIView , basename='semesterregistation')

