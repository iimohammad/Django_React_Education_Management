from django.urls import path
from .views import send_email_view

urlpatterns = [
    path('test-email/', send_email_view, name='send-email'),
]
