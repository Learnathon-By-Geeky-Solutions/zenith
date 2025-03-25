from django.urls import path
from api import views as api_views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path("user/token/", api_views.MyTokenObtainPairView.as_view()),
    path("register/", api_views.RegisterView.as_view()),
    path("user/token/refresh/", TokenRefreshView.as_view()),
]
