from rest_framework import viewsets, permissions
from .models import Assignment, AssignmentStatus
from .serializers import AssignmentSerializer, AssignmentStatusSerializer



class AssignmentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AssignmentSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return Assignment.objects.all()

class AssignmentStatusViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AssignmentStatusSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return AssignmentStatus.objects.all()