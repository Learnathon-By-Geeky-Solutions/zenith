from django.urls import path
from api import views as api_views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    #authentication endpoints
    path("user/token/", api_views.MyTokenObtainPairView.as_view()),
    path("register/", api_views.RegisterView.as_view()),
    path("user/token/refresh/", TokenRefreshView.as_view()),
     path("user/profile/<user_id>/", api_views.ProfileAPIView.as_view()),
    path("user/password-reset/<email>/", api_views.PasswordResetEmailVerifyAPIView.as_view()),
    path("user/password-change/", api_views.PasswordChangeAPIView.as_view()),
    path("user/change-password/", api_views.ChangePasswordAPIView.as_view()),


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
  
#getting cart total
path("cart/stats/<cart_id>/", api_views.CartStatsAPIView.as_view()),

#placing order url
 path("order/create-order/", api_views.CreateOrderAPIView.as_view()),

 #checkout url
 path("order/checkout/<oid>/", api_views.CheckoutAPIView.as_view()),

#apply cupon
 path("order/coupon/", api_views.CouponApplyAPIView.as_view()),

 #studeny summary 
  path("student/summary/<user_id>/", api_views.StudentSummaryAPIView.as_view()),

#course list api view
path("student/course-list/<user_id>/", api_views.StudentCourseListAPIView.as_view()),


#course detail api view
path("student/course-detail/<user_id>/<enrollment_id>/", api_views.StudentCourseDetailAPIView.as_view()),
#course completed api view
path("student/course-completed/", api_views.StudentCourseCompletedCreateAPIView.as_view()),

#note api
path("student/course-note/", api_views.StudentNoteCreateAPIView.as_view()),

path("student/rate-course/", api_views.StudentRateCourseCreateAPIView.as_view()),
path("student/review-detail/<user_id>/<review_id>/", api_views.StudentRateCourseUpdateAPIView.as_view()),
path("student/wishlist/<user_id>/", api_views.StudentWishListListCreateAPIView.as_view()),
]
