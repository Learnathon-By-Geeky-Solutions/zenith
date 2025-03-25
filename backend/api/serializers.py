from  rest_framework import serializers
from  userauths.models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['full_name'] = user.full_name
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["__all__"]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["__all__"]