from django.urls import path
from .views import *
urlpatterns = [
        path('detail/', AboutUsDetailView.as_view(), name='about_us_detail'),
        path('update/', AboutUsUpdateView.as_view(), name='about_us_update'),
        path('create/', AboutUsCreateView.as_view(), name='about_us_create'),
        path('delete/', AboutUsDeleteView.as_view(), name='about_us_delete'),
]
