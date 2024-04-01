from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import EmergencyRemovalRequestAPIView, EmploymentEducationRequestApiView, EnrollmentRequestApiView, RevisionRequestAPIView, SemesterCourseViewSet , StudentCoursesViewSet, StudentDeleteSemesterRequestAPIView, \
                    StudentExamsViewSet, StudentPassedCoursesViewSet, StudentProfileViewset , \
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
router.register('passed_courses' , StudentPassedCoursesViewSet , 
                basename='studentpassescourses')
router.register('student_exams' , StudentExamsViewSet , basename='studentexams')
router.register('semester_registration' , SemesterRegistrationRequestAPIView , 
                basename='semesterregistation')
router.register('unit_selection' , UnitSelectionRequestAPIView , basename='unitselection')
router.register('revision_request' , RevisionRequestAPIView , basename='revisionrequest')
router.register('emergency_remove_request' , EmergencyRemovalRequestAPIView , 
                basename='emergencyremoverequest')
router.register('delete_semester_request' , StudentDeleteSemesterRequestAPIView , 
                basename='deletesemesterrequest')
router.register('enrollment_request' , EnrollmentRequestApiView , 
                basename='enrollmentrequest')
router.register('employment_education_request' , EmploymentEducationRequestApiView , 
                basename='employmenteducationrequest')
# router.register('profile' , StudentProfileViewset , basename='profile')



urlpatterns = [
    path('', include(router.urls)),
    path('profile/' , StudentProfileViewset.as_view() , name='profile')
]
# handler404 = 'utils.error_views.handler404'