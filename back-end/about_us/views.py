from .serializers import *
from .models import *
from rest_framework import viewsets, permissions
from .permissions import IsAdminOrReadOnly


class ContactInfoViewSet(viewsets.ModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerialziers
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ('email','phone_number')


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializers
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ('name',)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated] 
    search_fields = ('content',)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True, author=self.request.user)
        return queryset

    def perform_create(self, serializer):

        author = self.request.user.username if self.request.user.is_authenticated else None
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author, is_active=False)
