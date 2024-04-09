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

urlpatterns = [
    path('', include(router.urls)),
    path('show-profile/', ShowProfileAPIView.as_view(), name='show_profile'),
    path('update-profile/',UserProfileUpdateAPIView.as_view(),name = 'update_profile'),
    path('semester_show/', ShowSemestersView.as_view({'get': 'list'}), name="semester_show"),
    # path('my_courses_semester/', SemesterCourseViewSet.as_view({'get': 'list'}), name="semester_courses"),
    path('AdvisorRole/ShowMyStudents/',ShowMyStudentsVeiw.as_view(),name = 'ShowMyStudents'),
    path('AdvisorRole/UnitSelectionRequest/',UnitSelectionRequestView.as_view(),name = 'UnitSelectionRequest'),

    path('AdvisorRole/SemesterRegistrationRequest/',SemesterRegistrationRequestView.as_view(),name = 'SemesterRegistrationRequest'),
    path('AdvisorRole/AddRemoveRequest/',AddRemoveRequestView.as_view(),name = 'AddRemoveRequest'),
    path('AdvisorRole/EmergencyRemovalRequest/',EmergencyRemovalRequestView.as_view(),name = 'EmergencyRemovalRequest'),
    path('AdvisorRole/StudentDeleteSemesterRequest/',StudentDeleteSemesterRequestView.as_view(),name = 'StudentDeleteSemesterRequest'),
    path('AdvisorRole/EnrollmentRequestView/',EnrollmentRequestView.as_view(),name = 'EnrollmentRequestView'),
    

]

