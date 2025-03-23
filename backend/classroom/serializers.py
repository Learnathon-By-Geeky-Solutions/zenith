from rest_framework import serializers
from .models import Classroom, Student


class ClassroomSerializer(serializers.ModelSerializer):
    ''' Serializes the Classroom model '''

    teacher = serializers.CharField(source = 'teacher.username', required = False, read_only = True)
    teacher_id = serializers.IntegerField(source = 'teacher.id', required = False, read_only = True)

    class Meta:
        model = Classroom
        fields = ('id', 'title','teacher', 'teacher_id', 'classroom_color')

class StudentSerializer(serializers.ModelSerializer):
    ''' Serializes the Student model '''

    classroom = serializers.CharField(source = 'classroom.title', required = False, read_only = True)
    classroom_id = serializers.IntegerField(source = 'classroom.id', required = False, read_only = True)
    student_id = serializers.IntegerField(source = 'id', required = False, read_only = True)
    
    class Meta:
        model = Student
        fields = ('student_id','classroom','classroom_id','students',)