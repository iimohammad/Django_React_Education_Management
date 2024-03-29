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
