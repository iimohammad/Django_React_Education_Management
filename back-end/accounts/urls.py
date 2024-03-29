from django.urls import path, reverse_lazy
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic.base import RedirectView
from .views import LogoutAPIView, RegisterUserApi, GenerateVerificationCodeView, PasswordResetActionView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutAPIView.as_view()),
    path('', RegisterUserApi.as_view()),
    path('change-password-request/', GenerateVerificationCodeView.as_view()),
    path('change-password-action/', PasswordResetActionView.as_view(), name='change-password-action'),

    # Google Login
]
