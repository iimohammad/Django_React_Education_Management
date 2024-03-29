from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from rest_framework.authtoken.views import ObtainAuthToken, obtain_auth_token

from .views import (LogoutAPIView, RegisterUserApi, google_auth_callback,
                    google_auth_redirect)

urlpatterns = [
    # path('login/', ObtainAuthToken.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('', RegisterUserApi.as_view()),
]
