from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


def generate_auth_token(user):
    ''' Generate a new token for the user '''
    token, created = Token.objects.get_or_create(user=user)
    return token


class TokenSerializer(serializers.Serializer):
    ''' Serializes the token '''

    token = serializers.CharField(max_length=255)


class LoginSerializer(serializers.Serializer):
    ''' Serializes the login request '''

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        ''' Validates the login request '''
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return data

    def get_token(self):
        ''' Returns the token for the user '''
        username = self.validated_data['username']
        user = User.objects.get(username=username)
        return TokenSerializer({
            'token': generate_auth_token(user)
        })


class RegisterSerializer(serializers.Serializer):
    ''' Serializes the registration request '''

    first_name=serializers.CharField(required=True, max_length=50)
    last_name=serializers.CharField(required=True, max_length=50)
    password = serializers.CharField(
        max_length=128, 
        min_length=8, 
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    email=serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=50)

    def validate_username(self, username):
        ''' Validates that username is unique '''
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists!")
        return username
    
    def validate_email(self, email):
        ''' Validates that email isn't already registered '''
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User already exists!")
        return email
    
    def register(self):
        ''' Register the user '''
        data=self.validated_data
        username=data['username']
        email=data['email']
        password=data['password']
        user=User.objects.create_user(username=username, email=email, password=password)
        user.first_name=data['first_name']
        user.last_name=data['last_name']
        user.save()

        return TokenSerializer({
            'token': generate_auth_token(user)
        })
    
class UserSerializer(serializers.ModelSerializer):
    ''' Serializes the user model '''

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email', 'password']

