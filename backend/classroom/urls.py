
from django.urls import path, include
from .import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'classroom', views.ClassroomViewSet, basename='classroom')


urlpatterns = [
    path(r'', include(router.urls)),
]