from django.contrib import admin
from django.urls import path , include
from config import local_settings
# from config.local_settings import *
from config.Sample_local_settings import *


urlpatterns = [
    path(local_settings.Admin, admin.site.urls),
    # path(Admin, admin.site.urls), 
    path("about_us/",include("about_us.urls")),
]
