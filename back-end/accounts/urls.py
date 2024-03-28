from django.urls import path, reverse_lazy
from .views import google_auth_redirect, google_auth_callback
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic.base import RedirectView
from .views import LogoutAPIView, RegisterUserApi
from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    # path('login/', ObtainAuthToken.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('', RegisterUserApi.as_view()),
]
