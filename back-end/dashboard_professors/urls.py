from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import  SemesterCourseViewSet, ShowMyStudentsVeiw, ShowSemestersView
from . import views

router = DefaultRouter()
router.register('TeacherRole/Semester-Show', ShowSemestersView, basename="SemesterShow")
router.register('TeacherRole/my-Courses-Semester', SemesterCourseViewSet,
                basename='SemesterCourse')

urlpatterns = [
    path('', include(router.urls)),
    path('show-profile/', views.ShowProfileAPIView.as_view(), name='show_profile'),
    path('update-profile/',views.UserProfileImageView.as_view(),name = 'update_profile'),
    path('AdvisorRole/ShowMyStudents/',ShowMyStudentsVeiw.as_view(),name = 'ShowMyStudents')
    path('AdvisorRole/UnitSelectionRequest/',UnitSelectionRequestView.as_view(),name = 'UnitSelectionRequest')

    path('AdvisorRole/SemesterRegistrationRequest/',SemesterRegistrationRequestView.as_view(),name = 'SemesterRegistrationRequest')
    path('AdvisorRole/AddRemoveRequest/',AddRemoveRequestView.as_view(),name = 'AddRemoveRequest')
    path('AdvisorRole/EmergencyRemovalRequest/',EmergencyRemovalRequestView.as_view(),name = 'EmergencyRemovalRequest')
    path('AdvisorRole/StudentDeleteSemesterRequest/',StudentDeleteSemesterRequestView.as_view(),name = 'StudentDeleteSemesterRequest')
    path('AdvisorRole/EnrollmentRequestView/',EnrollmentRequestView.as_view(),name = 'EnrollmentRequestView')

]

