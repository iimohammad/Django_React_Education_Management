from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer, EmailUserSerializer, PasswordResetActionSerializer, PasswordResetLoginSerializer
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




def google_auth_redirect(request):
    # Redirect to Google's OAuth2 authentication page
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    client_id = settings.GOOGLE_CLIENT_ID
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=email profile openid"
    return redirect(auth_url)

def google_auth_callback(request):
    # Handle Google's OAuth2 callback
    code = request.GET.get('code')
    if code:
        token_url = "https://accounts.google.com/o/oauth2/token"
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            # Use access_token to fetch user data from Google API
            # You can then authenticate the user in Django and redirect them to the appropriate page
            return "Authentication successful"
    return "Authentication failed"

@method_decorator(csrf_exempt, name= 'dispatch')
class GenerateVerificationCodeView(APIView):
    serializer_class = EmailUserSerializer

    def generate_verification_code(self):
        alphabet = string.ascii_letters + string.digits
        verification_code = ''.join(secrets.choice(alphabet) for _ in range(6))
        cache.set('code', f'{verification_code}', 3)
        return cache.get('code')

    def send_verification_code(self, email, verification_code):
        send_verification_code.delay(email, verification_code)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification_code = self.generate_verification_code()
            self.send_verification_code(email, verification_code)
            change_password_url = reverse_lazy('change-password-action')
            print(cache.get('code'))


            return Response({'message': 'Verification code sent successfully', 'change_password_url': change_password_url}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

def get_user_by_verification_code(code):
        code = cache.get('code')
        if code:
            try:
                user = User.objects.get(email=code.decode('utf-8'))
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
            new_password = serializer.validated_data['new_password']
            
            codes = cache.get('code')
            print(codes)
            if code == codes:
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
        

class ChangePasswordLoginView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = PasswordResetLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        


            

