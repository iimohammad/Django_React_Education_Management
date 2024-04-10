from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import  (
    AddRemoveRequestView,
    EmergencyRemovalConfirmationView,
    SemesterCourseViewSet,
    SemesterRegistrationRequestView,
    ShowMyStudentsVeiw, ShowSemestersView,
    StudentDeleteSemesterConfirmationAPI,
    UnitSelectionRequestView,
    ShowProfileAPIView,
    UserProfileImageView,
    EmploymentEducationConfirmationAPI,

)
from . import views

router = DefaultRouter()
router.register('TeacherRole/Semester-Show',
                ShowSemestersView,
                basename="SemesterShow")
router.register('TeacherRole/my-Courses-Semester',
                SemesterCourseViewSet,
                basename='SemesterCourse')


urlpatterns = [
    path('', include(router.urls)),
    
    path('show-profile/',
        ShowProfileAPIView.as_view(),
        name='show_profile'
        ),

    path('update-profile/',
        UserProfileImageView.as_view(),
        name = 'update_profile'
        ),
   
    path('AdvisorRole/ShowMyStudents/',
        ShowMyStudentsVeiw.as_view(),
        name = 'ShowMyStudents'
        ),
    
    path('AdvisorRole/UnitSelectionConfirmation/',
        UnitSelectionRequestView.as_view(),
        name = 'UnitSelectionConfirmation'
        ),

    path('AdvisorRole/SemesterRegistrationConfirmation/',
        SemesterRegistrationRequestView.as_view(),
        name = 'SemesterRegistrationRequest'
        ),

    path(
        'AdvisorRole/AddRemoveConfirmation/',
        AddRemoveRequestView.as_view(),
        name = 'AddRemoveConfirmation'
        ),
    path(
        'AdvisorRole/EmergencyRemovalConfirmation/',
        EmergencyRemovalConfirmationView.as_view(),
        name = 'EmergencyRemovalConfirmation'
        ),
    
    path('AdvisorRole/StudentDeleteConfirmation/',
        StudentDeleteSemesterConfirmationAPI.as_view(),
        name = 'StudentDeleteSemesterConfirmation'
        ),
    
    path(
        'AdvisorRole/EmploymentEducationConfirmation/',
        EmploymentEducationConfirmationAPI.as_view(),
        name = 'EmploymentEducationConfirmation'
        ),
]

