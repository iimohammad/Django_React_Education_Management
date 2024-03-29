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
# from rest_framework.views import LoginView
from accounts.models import User

from .serializers import ProfileSerializer, RegisterSerializer, UserSerializer


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
        return Response({"user": UserSerializer(
            user, context=self.get_serializer_context()).data, "token": token.key})

@method_decorator(csrf_exempt, name= 'dispatch')
class GenerateVerificationCodeView(APIView):
    serializer_class = EmailUserSerializer

    def generate_verification_code(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(6))
    print(generate_verification_code)

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
            change_password_url = reverse_lazy('change-password-action')

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
        

class ChangePasswordLoginView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = PasswordResetLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        


            

def google_auth_redirect(request):
    # Redirect to Google's OAuth2 authentication page
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    client_id = settings.GOOGLE_CLIENT_ID
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={
        client_id}&redirect_uri={redirect_uri}&response_type=code&scope=email profile openid"
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
            # You can then authenticate the user in Django and redirect them to
            # the appropriate page
            return "Authentication successful"
    return "Authentication failed"


# Change Profile implement Here
class change_profile(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer()
    queryset = User.objects.all()


class CustomLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully'}, status=200)

    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('rest_framework:login'))
