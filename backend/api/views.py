from django.shortcuts import render
from api import serializers as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from userauths.models import User, Profile
from rest_framework.permissions import AllowAny
import random
# this view is for token generation
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer
'''when someone geos to  register endpoint it will come to this endpoint
and it will allow any user to use this endpoint'''


class RegisterView(generics.CreateAPIView):
     queryset = User.objects.all()
     permission_classes = [AllowAny] #allows any user to use this endpoint
     serializer_class = api_serializer.RegisterSerializer
#method to generate otp
def generate_random_otp(length=7):
    otp="".join([str(random.randint(0,9)) for _ in range(length)])
    return otp

#how to reset password
class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes=[AllowAny]
    serializer_class=api_serializer.UserSerializer # user model will be modified so we need the serializer to be modified

    def get_object(self):
        email=self.kwargs['email'] #Grabs the email from the URL
        user=User.objects.filter(email=email).first()
        if user:
            user.otp="1234"