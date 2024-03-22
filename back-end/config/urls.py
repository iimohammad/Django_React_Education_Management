from django.contrib import admin
from django.urls import path,include
from config import local_settings


urlpatterns = [
    # Admin Urls
    path(local_settings.Admin, admin.site.urls),
]
