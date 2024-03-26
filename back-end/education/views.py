from rest_framework import viewsets , generics
from accounts.models import Student , Teacher
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import StudentFilter , TeacherFilter
from .pagination import DefaultPagination
from .permissions import IsEducationalAssistant
from rest_framework.permissions import IsAuthenticated

class 
