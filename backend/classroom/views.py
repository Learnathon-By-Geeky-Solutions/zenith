from rest_framework import viewsets, permissions
from .models import Classroom, Student
from .serializers import ClassroomSerializer, StudentSerializer

class ClassroomViewSet(viewsets.ModelViewSet):
    ''' Handles the CRUD operations on Classroom model '''

    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        ''' Assigns the teacher to the classroom '''
        serializer.save(teacher=self.request.user)

class StudentViewSet(viewsets.ModelViewSet):
    ''' Handles the CRUD operations on Student model '''
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)
