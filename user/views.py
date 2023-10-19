from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UserSerializer
from .models import User

from django.contrib.auth import authenticate

from json import loads as Json_load
from datetime import datetime

class RegisterUserview(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['post']

class UserLoginView(viewsets.ModelViewSet):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    serializer_class = UserSerializer
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        user = authenticate(**request.data)
        if user:
            serializer = self.get_serializer(user)
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"Message":"Invalid Email or password"}, status=status.HTTP_400_BAD_REQUEST)

class UserlogoutView(viewsets.ViewSet):
    """
    An endpoint to logout users.
    """
    http_method_names = ['post']

    def create(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)