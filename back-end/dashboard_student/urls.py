from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import  (
                    AddRemoveRequestAPIView,
                    CourseViewSet, 
                    EmergencyRemovalRequestAPIView,
                    EmploymentEducationRequestApiView,
                    RevisionRequestAPIView, 
                    SemesterCourseViewSet, 
                    StudentCoursesViewSet, 
                    StudentDeleteSemesterRequestAPIView,
                    StudentExamsViewSet, 
                    StudentPassedCoursesViewSet, 
                    StudentProfileViewset,
                    SemesterRegistrationRequestAPIView,
                    UnitSelectionRequestAPIView,
                    )


router = DefaultRouter()


router.register('courses' , CourseViewSet , basename='courses')
router.register('semester_courses' , SemesterCourseViewSet , basename='semestercourses')
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

router.register('employment_education_request' , EmploymentEducationRequestApiView , 
                basename='employmenteducationrequest')

router.register('AddRemoveRequestViewSet',AddRemoveRequestAPIView,basename='AddRemoveRequestViewSet')


urlpatterns = [
    path('', include(router.urls)),
    path('profile/' , StudentProfileViewset.as_view() , name='profile')
]