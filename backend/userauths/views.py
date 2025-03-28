from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from . import serializers as user_serializers
from .models import User, Profile

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = user_serializers.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_serializers.RegisterSerializer