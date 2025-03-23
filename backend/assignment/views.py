from rest_framework import viewsets, permissions
from .models import Assignment, AssignmentStatus
from .serializers import AssignmentSerializer, AssignmentStatusSerializer



class AssignmentViewSet(viewsets.ModelViewSet):
    ''' Handles creating, reading and updating assignments '''

    queryset = Assignment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AssignmentSerializer

    def create(self, request, *args, **kwargs):
        ''' Create a new assignment '''
        return super().create(request, *args, **kwargs)

class AssignmentStatusViewSet(viewsets.ModelViewSet):
    ''' Handles creating, reading and updating assignment statuses '''

    queryset = AssignmentStatus.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AssignmentStatusSerializer

    def create(self, request, *args, **kwargs):
        ''' Update the status of an assignment '''
        return super().create(request, *args, **kwargs)
