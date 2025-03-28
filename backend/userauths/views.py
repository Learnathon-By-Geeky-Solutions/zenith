import random
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers as user_serializers
from .models import User, Profile

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = user_serializers.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_serializers.RegisterSerializer

def generate_random_otp(length=7):
    otp = ''.join(str(random.randint(0, 9)) for _ in range(length))
    return otp

class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = user_serializers.UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects. filter(email=email).first()
        if user:
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()
            link = f'http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&=refresh_token{refresh_token}'
        return user

class PasswordChangeAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = user_serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        otp = request.data['otp']
        uuidb64 = request.data['uuidb64']
        password = request.data['password']
        user = User.objects.get(id=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ''
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': "User Doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
