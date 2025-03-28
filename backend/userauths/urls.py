from django.urls import path
from . import views as api_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', api_views.MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', api_views.RegisterView.as_view()),
    path('password-reset/<email>', api_views.PasswordResetEmailVerifyAPIView.as_view()),
    path('password-change/', api_views.PasswordChangeAPIView.as_view()),
]
