from django.urls import path
from .views import AboutUsDetailView, AboutUsCreateView, AboutUsUpdateView, AboutUsDeleteView

urlpatterns = [
    path('<int:university_id>/about/', AboutUsDetailView.as_view(), name='about_us_detail'),
    path('<int:university_id>/about/create/', AboutUsCreateView.as_view(), name='about_us_create'),
    path('<int:university_id>/about/update/', AboutUsUpdateView.as_view(), name='about_us_update'),
    path('<int:university_id>/about/delete/', AboutUsDeleteView.as_view(), name='about_us_delete'),
    path('<int:university_id>/about/delete/', AboutUsDeleteView.as_view(), name='about_us_delete')
]
