from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import  (
    AddRemoveRequestView,
    EmergencyRemovalRequestView,
    EnrollmentRequestView,
    SemesterCourseViewSet,
    SemesterRegistrationRequestView,
    ShowMyStudentsVeiw, 
    ShowSemestersView,
    StudentDeleteSemesterRequestView,
    UnitSelectionRequestView,
    ShowProfileAPIView,
    UserProfileUpdateAPIView,
    RevisionRequestView,
)

router = DefaultRouter()
router.register('my_courses_semester' , SemesterCourseViewSet,basename='semester_courses')
router.register('revision_requests' , RevisionRequestView,basename='revision_requests')
router.register('unit_selection_requests' , RevisionRequestView,basename='unit_selection')
router.register('semester_registration_requests' , SemesterRegistrationRequestView,basename='semester_registration')


urlpatterns = [
    path('', include(router.urls)),
    path('show-profile/', ShowProfileAPIView.as_view(), name='show_profile'),
    path('update-profile/',UserProfileUpdateAPIView.as_view(),name = 'update_profile'),
    path('semester_show/', ShowSemestersView.as_view({'get': 'list'}), name="semester_show"),
    path('show_my_students/',ShowMyStudentsVeiw.as_view(),name = 'showmystudents'),
    path('AddRemoveRequest/',AddRemoveRequestView.as_view(),name = 'AddRemoveRequest'),
    path('EmergencyRemovalRequest/',EmergencyRemovalRequestView.as_view(),name = 'EmergencyRemovalRequest'),
    path('StudentDeleteSemesterRequest/',StudentDeleteSemesterRequestView.as_view(),name = 'StudentDeleteSemesterRequest'),
    path('EnrollmentRequestView/',EnrollmentRequestView.as_view(),name = 'EnrollmentRequestView'),
]

