from rest_framework.routers import DefaultRouter
from .views import ContactInfoViewSet, UniversityViewSet , CommentViewSet
from django.urls import path, include

router = DefaultRouter()  

router.register('ContactInfo', ContactInfoViewSet, basename='ContactInfo') 
router.register('University',UniversityViewSet,basename='University')
router.register('Comment',CommentViewSet,basename='Comment')

urlpatterns = [
    path('', include(router.urls)),  
]