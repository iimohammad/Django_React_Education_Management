from django.contrib import admin
import os
import dotenv
dotenv.read_dotenv()

from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from accounts.permissions import (IsAdmin, IsEducationalAssistant, IsStudent,
                                  IsTeacher)
from accounts.views import CustomLogoutView
from home.views import login
from utils.error_views import custom_404

# Authentication URLs
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', CustomLogoutView.as_view(), name='custom_logout'),
    path('', login),
    path('', include('rest_framework.urls')),
    path('home/',include('home.urls')),
]

# URLs for different user roles
if IsAdmin:
    urlpatterns += [
        # Admin URLs
        path(os.environ.get('Admin'), admin.site.urls),
        # App URLs
        path(
            'academic_events/',
            include('academic_events.urls'),
            name='accounts'),
        path('accounts/', include('accounts.urls'), name='accounts'),
        path('admin/', include('admin_dashboard_panel.urls',
             namespace='admin_dashboard')),
        # Swagger URLs
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/swagger-ui/',
             SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/',
             SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        path('dashboard_student/', include('dashboard_student.urls'),
             name='dashboard_student'),
        path('dashboard_professors/', include('dashboard_professors.urls'),
             name='dashboard_professors'),
        path('dashboard_educationalassistant/', include('dashboard_educationalassistant.urls'),
             name='dashboard_educationalassistant'),
    ]
if IsStudent:

    urlpatterns += [
        path('dashboard_student/', include('dashboard_student.urls'),
             name='dashboard_student'),
    ]

if IsTeacher:
    urlpatterns += [
        path('dashboard_professors/', include('dashboard_professors.urls'),
             name='dashboard_professors'),
    ]

if IsEducationalAssistant():
    urlpatterns += [path('dashboard_educationalassistant/',
                         include('dashboard_educationalassistant.urls'),
                         name='dashboard_educationalassistant'),
                    ]

# Debug Toolbar URLs
if os.environ.get('USE_DEBUG_TOOLBAR')  :
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

# handler404 = 'utils.error_views.custom_404'
