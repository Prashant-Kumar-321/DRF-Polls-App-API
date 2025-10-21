from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User

from .user_serializers import UserCreateSerializer

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
