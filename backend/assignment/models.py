from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from classroom.models import Classroom

# Create your models here.

class Assignment(models.Model):
    ''' Assignment model '''

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=255)
    deadline = models.DateTimeField(default=datetime.now, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null = True)
    
    # Score choices codes:
    UNGRADED = 0
    POOR = 1
    BELOW_AVERAGE = 2
    AVERAGE = 3
    GOOD = 4
    EXCELLENT = 5

    SCORE_CHOICES = (
        (UNGRADED, 'Ungraded'),
        (str(POOR), ('1 - Very Poor')),
        (str(BELOW_AVERAGE), ('2 - Below Average')),
        (str(AVERAGE), ('3 - Average')),
        (str(GOOD), ('4 - Good')),
        (str(EXCELLENT), ('5 - Excellent'))
    )

    score = models.BooleanField(choices=SCORE_CHOICES, default=False)

    def __str__(self):
        return self.title
    

class AssignmentStatus(models.Model):
    ''' Assignment status model '''

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null = True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    BOOL_CHOICES = ((True, 'Completed'), (False, 'Incomplete'))
    status = models.BooleanField(choices=BOOL_CHOICES, default=False)

    def __str__(self):
        return self.student.username

