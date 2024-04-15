import requests
from django.contrib.auth import logout
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserProfileImageSerializer, UserSerializer, EmailUserSerializer, \
    PasswordResetActionSerializer, PasswordResetLoginSerializer, UserChangePassSerializer
from django.conf import settings
from django.utils import timezone
import string
import redis
from django.http import JsonResponse
from .tasks import send_verification_code, send_Password_Changed
import secrets
from rest_framework.reverse import reverse_lazy
from .models import User
from .versioning import DefualtVersioning
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from .permissions import IsNotAuthenticated

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={'message': f'Bye {request.user.username}!'},
            status=status.HTTP_204_NO_CONTENT
        )


class RegisterUserApi(generics.GenericAPIView):
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return RegisterSerializer
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({"user": UserSerializer(
            user, context=self.get_serializer_context()).data, "token": token.key})


class GenerateVerificationCodeView(APIView):
    versioning_class = DefualtVersioning
    serializer_class = UserChangePassSerializer 

    def generate_verification_code(self):
        alphabet = string.ascii_letters + string.digits
        verification_code = ''.join(secrets.choice(alphabet) for _ in range(6))
        return verification_code

    def send_verification_code(self, email, verification_code):
        send_verification_code.delay(email, verification_code)

    def post(self, request):
        email = request.data.get('email')
        last_request_time = cache.get(email + '_last_request_time')
        current_time = timezone.now()

        if last_request_time and (current_time - last_request_time).seconds < 120:
            remaining_time = 120 - (current_time - last_request_time).seconds
            return Response({'message': f'Please wait for {remaining_time} seconds before trying again.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            verification_code = self.generate_verification_code()
            self.send_verification_code(email, verification_code)
            cache.set(email + '_verification_code', verification_code, 120)  
            cache.set(email + '_last_request_time', current_time, 120)  
            user = User.objects.get(email=email)
            return redirect('change-password-action', user_id=user.id)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetActionView(APIView):
    permission_classes = [IsNotAuthenticated]
    versioning_class = DefualtVersioning
    serializer_class = PasswordResetActionSerializer

    def send_Password_Changed(self,email):
        send_Password_Changed.delay(email)

    def post(self, request, user_id):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']
        user = User.objects.get(id=user_id)
        email = user.email 
        cached_code = cache.get(email + '_verification_code')  #
        if code != cached_code:
            return Response({'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        self.send_Password_Changed(email)
        return redirect('login')

class ChangePasswordLoginView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordResetLoginSerializer

    def send_Password_Changed(self,email):
        send_Password_Changed.delay(email)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            user_email = request.user.email 
            self.send_Password_Changed(user_email)
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully'}, status=200)

    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('rest_framework:login'))


class UserProfileImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return UserProfileImageSerializer
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        user_instance = self.get_object()
        serializer.save(instance=user_instance)
