from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers as user_serializers

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = user_serializers.MyTokenObtainPairSerializer
