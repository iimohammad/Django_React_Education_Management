from django.contrib import admin
from django.urls import path,include
from config import local_settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from home.views import home
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    # Admin Urls
    path(local_settings.Admin, admin.site.urls),
    # Home
    path('', home),
    # App Urls
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('admin/', include('admin_dashboard_panel.urls'), name='admin_dashboard'),
    path('dashboard_student/', include('dashboard_student.urls'), name='dashboard_student'),
    # path('about_us/', include('about_us.urls')),
    # Authentication URLS
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls')),
    #DashboardEducationalAssistant
    path('dashboard_educationalassistant/',include('dashboard_educationalassistant.urls'), name='dashboard_educationalassistant'),
    #swagger
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
