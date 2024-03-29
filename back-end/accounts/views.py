from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer, EmailUserSerializer, PasswordResetActionSerializer
from django.conf import settings
import requests
import string
import redis
from django.conf import settings
from django.http import JsonResponse
from .tasks import send_verification_code
import secrets
from django.urls import reverse
from .models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={'message': f'Bye {request.user.username}!'},
            status=status.HTTP_204_NO_CONTENT
        )


class RegisterUserApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })



@method_decorator(csrf_exempt, name= 'dispatch')
class GenerateVerificationCodeView(APIView):
    serializer_class = EmailUserSerializer

    def generate_verification_code(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(6))

    def store_verification_code_in_redis(self, email, verification_code):
        redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        redis_client.setex(email, 40, verification_code)

    def send_verification_code(self, email, verification_code):
        send_verification_code.delay(email, verification_code)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification_code = self.generate_verification_code()
            print(verification_code)
            self.store_verification_code_in_redis(email, verification_code)
            self.send_verification_code(email, verification_code)
            change_password_url = reverse('change-password-action')

            return Response({'message': 'Verification code sent successfully', 'change_password_url': change_password_url}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

def get_user_by_verification_code(code):
        redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        email = redis_client.get(code)
        if email:
            try:
                user = User.objects.get(email=email.decode('utf-8'))
                return user
            except User.DoesNotExist:
                return None
        else:
            return None
class PasswordResetActionView(APIView):
    serializer_class = PasswordResetActionSerializer
    
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            print(code)
            new_password = serializer.validated_data['new_password']
            
            redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
            stored_code = redis_client.get('mohammadbaharloo97@yahoo.com')
            print(stored_code)
            if stored_code and stored_code.decode('utf-8') == code:
                user = get_user_by_verification_code(code)
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



        


            

