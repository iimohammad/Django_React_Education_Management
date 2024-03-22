from django.urls import path
from .views import google_auth_redirect, google_auth_callback
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserRegistration, LogoutAPIView

urlpatterns = [
    # path('login/', obtain_auth_token, name='login'),
    # path('logout/', LogoutAPIView.as_view()),
    # path('register/', UserRegistration.as_view()),

    # Google Login
    path('google-auth/', google_auth_redirect, name='google_auth_redirect'),
    path('google-auth/redirect/', google_auth_callback, name='google_auth_callback'),

]
