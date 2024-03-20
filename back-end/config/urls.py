from django.contrib import admin
from django.urls import path
from config import local_settings


urlpatterns = [
    path(local_settings.Admin, admin.site.urls),
]
