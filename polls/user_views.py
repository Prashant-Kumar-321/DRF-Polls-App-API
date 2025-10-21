from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response

from .user_serializers import UserCreateSerializer

class CreateUser(generics.CreateAPIView):
    """Create a new user """

    # User does not need to be authenticated
    authentication_classes = []
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class LoginUser(APIView): 
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)

        if not user: 
            return Response(
                data={
                    'error': "Invalid user credentials"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
        return  Response(
            data={
                "token": user.auth_token.key
            },
            status=status.HTTP_200_OK
        )  


