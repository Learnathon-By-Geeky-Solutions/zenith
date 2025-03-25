from django.shortcuts import render
from api import serializers as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from userauths.models import User, Profile
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import random

# this view is for token generation
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer
'''when someone geos to  register endpoint it will come to this endpoint
and it will allow any user to use this endpoint'''

#end point to register a user
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
        email=self.kwargs['email'] #Grabs the email from the URL. for this in the url we need <email>
        user=User.objects.filter(email=email).first()
        if user:
           
            uuidb64=user.pk
            refresh=RefreshToken.for_user(user)
            refresh_token=str(refresh.access_token)
            user.refresh_token=refresh_token
            user.otp=generate_random_otp()
            user.save() # we want to save the otp for the user so using save method
            link=f"http://localhost:3000/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&=refresh_token={refresh_token}"
            print("link=",link)
            return user
        return None
    

class PasswordChangeAPIView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=api_serializer.UserSerializer
   
    def create(self, request, *args, **kwargs):
        payload=request.data
        otp=payload['otp']
        uuidb64=payload['uuidb64']
        password=payload['password']

        user=User.objects.get(id=uuidb64,otp=otp)
        if user:
            user.set_password(password)
            user.otp=""
            user.save()
            return Response({"message":"password changed successfully"},status=200)
        else:
            return Response({"message":"user doesn't exist"},status=400)
 
