from django.urls import path
from api import views as api_views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    #authentication endpoints
    path("user/token/", api_views.MyTokenObtainPairView.as_view()),
    path("register/", api_views.RegisterView.as_view()),
    path("user/token/refresh/", TokenRefreshView.as_view()),\
    path("user/password-reset/<email>/", api_views.PasswordResetEmailVerifyAPIView.as_view()),
    path("user/password-change/", api_views.PasswordChangeAPIView.as_view()),

    #course endpoints
    path("course/category/", api_views.CategoryListAPIView.as_view()),
    path("course/course-list/", api_views.CourseListAPIView.as_view()),
     path("course/course-detail/<slug>", api_views.CourseDetailAPIView.as_view()),

     #adding items to cart url
    path("course/cart/", api_views.CartAPIView.as_view()),

    #getting cart-list
    path("course/cart-list/<cart_id>/", api_views.CartListAPIView.as_view()),
  
  #deleting cart item
  path("course/cart-item-delete/<cart_id>/<item_id>/", api_views.CartItemDeleteAPIView.as_view()),

]
