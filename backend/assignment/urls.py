from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, AssignmentStatusViewSet

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'assignment-status', AssignmentStatusViewSet, basename='assignment-status')

urlpatterns = [
    path(r'', include(router.urls)),
]