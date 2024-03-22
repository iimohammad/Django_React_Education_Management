from django.contrib import admin
<<<<<<< HEAD
from django.urls import path,include
=======
from django.urls import path, include
>>>>>>> 2a8ee34cd1303c33b5151441d0aa994874073eab
from config import local_settings


urlpatterns = [
    # Admin Urls
    path(local_settings.Admin, admin.site.urls),
<<<<<<< HEAD
=======

    # App Urls
    path('accounts/', include('accounts.urls'), name='blog'),
    # Authentication URLS
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls')),
>>>>>>> 2a8ee34cd1303c33b5151441d0aa994874073eab
]
