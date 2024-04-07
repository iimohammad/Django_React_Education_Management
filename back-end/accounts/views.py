import requests
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserProfileImageSerializer, UserSerializer, EmailUserSerializer, \
    PasswordResetActionSerializer, PasswordResetLoginSerializer
from django.conf import settings
import requests
import string
import redis
from django.conf import settings
from django.http import JsonResponse
from .tasks import send_verification_code
import secrets
from rest_framework.reverse import reverse_lazy
from .models import User
from .versioning import DefualtVersioning
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache


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


@method_decorator(csrf_exempt, name='dispatch')
class GenerateVerificationCodeView(APIView):
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return EmailUserSerializer

    def generate_verification_code(self):
        alphabet = string.ascii_letters + string.digits
        verification_code = ''.join(secrets.choice(alphabet) for _ in range(6))
        cache.set('code', f'{verification_code}', 360)
        return cache.get('code')

    def send_verification_code(self, email, verification_code):
        send_verification_code.delay(email, verification_code)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email_in = serializer.validated_data['email']
            verification_code = self.generate_verification_code()
            self.send_verification_code(email_in, verification_code)
            user = User.objects.get(email=email_in)
            return redirect('change-password-action', user_id=user.id)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetActionView(APIView):
    versioning_class = DefualtVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return PasswordResetActionSerializer

    def post(self, request, user_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']
            user = User.objects.get(id=user_id)
            codes = cache.get('code')

            if code == codes:
                if user:
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordLoginView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PasswordResetLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
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
