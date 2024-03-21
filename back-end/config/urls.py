from django.contrib import admin
from django.urls import path , include
from config import local_settings


urlpatterns = [
    path(local_settings.Admin, admin.site.urls),
    path("about_us/",include("about_us.urls")),
]
