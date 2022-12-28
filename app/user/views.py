"""Views of the user API"""

from django.shortcuts import render

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer

# Create your views here.
class UserApiView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer

class CreateUserTokenApiView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    # renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user"""

        return self.request.user