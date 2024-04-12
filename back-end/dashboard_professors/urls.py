from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import  (
    AddRemoveRequestView,
    EmergencyRemovalConfirmationView,
    EvaluateStudentsAPIView,
    EvaluateStudentsViewSet,
    RevisionRequestView,
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

router.register('AdvisorRole/StudentDeleteSemesterConfirmation',
                StudentDeleteSemesterConfirmationAPI,
                basename='StudentDeleteSemesterConfirmation')

router.register('AdvisorRole/SemesterRegistrationConfirmation',
                SemesterRegistrationConfirmationViewAPI,
                basename='SemesterRegistrationRequest')

router.register('AdvisorRole/EmploymentEducationConfirmation',
                EmploymentEducationConfirmationAPI,
                basename='EmploymentEducationConfirmation')


router.register('AdvisorRole/AddRemoveConfirmation',
                AddRemoveRequestView,
                basename='AddRemoveConfirmation')

router.register('AdvisorRole/ShowMyStudents/',
                ShowMyStudentsVeiw,
                basename='ShowMyStudents')

router.register(
    'evaluate',
    EvaluateStudentsViewSet,
    basename='evaluate-courses')

router.register('revision-requests',
                RevisionRequestView,
                basename='revision-request')

urlpatterns = [
    path('', include(router.urls)),
    
    path('show-profile/',
        ShowProfileAPIView.as_view(),
        name='show_profile'
        ),

   

    
    path('AdvisorRole/UnitSelectionConfirmation/',
        UnitSelectionRequestView.as_view(),
        name = 'UnitSelectionConfirmation'
        ),
    path('evaluate-students/', EvaluateStudentsAPIView.as_view(), name='evaluate_students'),

]