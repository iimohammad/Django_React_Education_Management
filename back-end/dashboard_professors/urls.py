from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import  (
    AddRemoveRequestView,
    EmergencyRemovalConfirmationView,
    SemesterCourseViewSet,
    SemesterRegistrationConfirmationViewAPI,
    ShowMyStudentsVeiw, ShowSemestersView,
    StudentDeleteSemesterConfirmationAPI,
    UnitSelectionRequestView,
    ShowProfileAPIView,
    EmploymentEducationConfirmationAPI,

)

router = DefaultRouter()
router.register('TeacherRole/Semester-Show',
                ShowSemestersView,
                basename="SemesterShow")

router.register('TeacherRole/my-Courses-Semester',
                SemesterCourseViewSet,
                basename='SemesterCourse')

router.register('AdvisorRole/EmergencyRemovalConfirmation',
                EmergencyRemovalConfirmationView,
                basename='EmergencyRemovalConfirmation')

router.register('AdvisorRole/StudentDeleteConfirmation',
                StudentDeleteSemesterConfirmationAPI,
                basename='StudentDeleteSemesterConfirmation')

router.register('AdvisorRole/SemesterRegistrationConfirmation',
                SemesterRegistrationConfirmationViewAPI,
                basename='SemesterRegistrationRequest')

router.register('AdvisorRole/EmploymentEducationConfirmation',
                EmploymentEducationConfirmationAPI,
                basename='EmploymentEducationConfirmation')
urlpatterns = [
    path('', include(router.urls)),
    
    path('show-profile/',
        ShowProfileAPIView.as_view(),
        name='show_profile'
        ),

   
    path('AdvisorRole/ShowMyStudents/',
        ShowMyStudentsVeiw.as_view(),
        name = 'ShowMyStudents'
        ),
    
    path('AdvisorRole/UnitSelectionConfirmation/',
        UnitSelectionRequestView.as_view(),
        name = 'UnitSelectionConfirmation'
        ),

    path(
        'AdvisorRole/AddRemoveConfirmation/',
        AddRemoveRequestView.as_view(),
        name = 'AddRemoveConfirmation'
        ),
    
   
]