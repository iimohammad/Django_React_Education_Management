from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import SemesterCourseViewSet , StudentCoursesViewSet, \
                    StudentExamsViewSet, StudentProfileViewset , \
                    SemesterRegistrationRequestAPIView, UnitSelectionRequestAPIView
# from .views import (StudentViewSet,
#                     TeacherViewSet,
#                     EnrollmentRequestViewSet,
#                     SemesterCourseViewSet,
#                     StudentCoursesViewSet,
#                     )

router = DefaultRouter()

# router.register("EucationalAssistantPanel/Students", StudentViewSet, basename="Student")
# router.register("EucationalAssistantPanel/Teachers", TeacherViewSet, basename="teacher")
# router.register("EucationalAssistantPanel/Course", CourseViewSet, basename="Course")
# router.register("EucationalAssistantPanel/SemesterCourse", SemesterCourseViewSet, basename="SemesterCourse")

# router.register(r'enrollment-requests', EnrollmentRequestViewSet,basename='enrollment')



router.register('semester_courses' , SemesterCourseViewSet , basename='semestercourse')
router.register('student_courses' , StudentCoursesViewSet , basename='studentcourses')
router.register('student_exams' , StudentExamsViewSet , basename='studentexams')
router.register('semester_registration' , SemesterRegistrationRequestAPIView , basename='semesterregistation')
router.register('unit_selection' , UnitSelectionRequestAPIView , basename='unitselection')
# router.register('profile' , StudentProfileViewset , basename='profile')



urlpatterns = [
    path('', include(router.urls)),
    path('profile/' , StudentProfileViewset.as_view() , name='profile')
]