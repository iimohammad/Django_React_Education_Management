from django.contrib import admin
from django.urls import path, include
from config import local_settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    # Admin Urls
    path(local_settings.Admin, admin.site.urls),
    

    # App Urls
    path('accounts/', include('accounts.urls'), name='blog'),
    path('about_us/', include('about_us.urls')),
    # Authentication URLS
    # Authentication URLS
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls')),
]
