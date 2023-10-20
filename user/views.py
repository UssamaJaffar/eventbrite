from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UserSerializer
from .models import User

from django.contrib.auth import authenticate

from Event.settings import EVENTBRITE_TOKEN

import requests

class RegisterUserview(viewsets.ModelViewSet):
    """
    A viewset for creating user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['post']

    def create(self, request):
        """
        Get the user information from the eventbrite and store the data with required fields into database
        """
        try:
            response = requests.get('https://www.eventbriteapi.com/v3/users/me/', headers={"Content-Type":"text" , "Authorization": f"Bearer {EVENTBRITE_TOKEN}"})
            if response.status_code == 200:

                request.data['user_id'] = response.json()['id']
                response = requests.get('https://www.eventbriteapi.com/v3/users/me/organizations/', headers={"Content-Type":"text" , "Authorization": f"Bearer {EVENTBRITE_TOKEN}"})

                if response.status_code == 200:
                    request.data['organization_id'] = response.json()['organizations'][0]['id']

                    serializer = self.serializer_class(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    return Response({"response":serializer.validated_data}, status=status.HTTP_200_OK)

                else:
                    return Response({"Message":"Something went wrong! Try again"}, status=status.HTTP_400_BAD_REQUEST)
        
            else:
                return Response({"Message":"Something went wrong! Try again"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Message":"Intenal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLoginView(viewsets.ModelViewSet):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    serializer_class = UserSerializer
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        try:

            user = authenticate(**request.data)
            if user:
                serializer = self.get_serializer(user)
                data = serializer.data

                token = RefreshToken.for_user(user)
                data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
                return Response(data, status=status.HTTP_200_OK)

            else:
                return Response({"Message":"Invalid Email or password"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Message":"Intenal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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