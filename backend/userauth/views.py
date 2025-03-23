from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    LoginSerializer, 
    RegisterSerializer,
    UserSerializer
)

# Create your views here.

class RegisterView(APIView):
    ''' Handles the registration of a new user '''

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.register()
        return Response(response.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    ''' Handles the login of a user '''

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.get_token()
        return Response(response.data, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    ''' Handles the profile view of a user'''

    permission_classes = [(permissions.IsAuthenticated,)]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
