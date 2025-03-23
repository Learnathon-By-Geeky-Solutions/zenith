from rest_framework import serializers
from .models import Assignment, AssignmentStatus

class AssignmentSerializer(serializers.ModelSerializer):
    ''' Serializes the Assignment model '''

    teacher = serializers.CharField(source = 'teacher.username', required = False, read_only = True)
    assignment_id = serializers.IntegerField(source = 'assignment.id', required = False, read_only = True)
    classroom = serializers.CharField(source = 'classroom.title', required = False, read_only = True)
    classroom_id = serializers.IntegerField(source = 'classroom.id', required = False, read_only = True)

    class Meta:
        model = Assignment
        fields = ('assignment_id','title','teacher','classroom','classroom_id','deadline','score',)

class AssignmentStatusSerializer(serializers.ModelSerializer):
    ''' Serializes the AssignmentStatus model '''

    student = serializers.CharField(source = 'student.username', required = False, read_only = True)
    student_id = serializers.IntegerField(source = 'student.id', required = False, read_only = True)
    assignment = serializers.CharField(source = 'assignment.title', required = False, read_only = True)
    assignment_id = serializers.IntegerField(source = 'assignment.id', required = False, read_only = True)
    
    class Meta:
        model = AssignmentStatus
        fields = ('assignment_id','assignment','student','student_id','status',)