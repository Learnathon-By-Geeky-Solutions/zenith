from django.shortcuts import render
from api import serializers as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from userauths.models import User, Profile
from rest_framework.permissions import AllowAny

# this view is for token generation
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer
'''when someone geos to  register endpoint it will come to this endpoint
and it will allow any user to use this endpoint'''
class RegiserView(generics.CreateAPIView):
     queryset = User.objects.all()
     permission_classes = [AllowAny] #allows any user to use this endpoint
     serializer_class = api_serializer.RegisterSerializer