from django.urls import path, reverse_lazy
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic.base import RedirectView
from .views import LogoutAPIView, RegisterUserApi, GenerateVerificationCodeView, PasswordResetActionView
from django.views.generic.base import RedirectView
from rest_framework.authtoken.views import ObtainAuthToken, obtain_auth_token

from .views import (LogoutAPIView, RegisterUserApi, google_auth_callback,google_auth_redirect)

from .views import LogoutAPIView, RegisterUserApi, GenerateVerificationCodeView, PasswordResetActionView, ChangePasswordLoginView

urlpatterns = [
    # path('login/', ObtainAuthToken.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('', RegisterUserApi.as_view()),
    path('change-password-request/', GenerateVerificationCodeView.as_view()),
    path('change-password-action/<int:user_id>/', PasswordResetActionView.as_view(), name='change-password-action'),
    path('password-change-login/',ChangePasswordLoginView.as_view()),


]
