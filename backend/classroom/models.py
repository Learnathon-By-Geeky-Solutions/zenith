from django.db import models
from django.contrib.auth.models import User


class Classroom(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)

    # Color choices code
    BLUE = 0
    RED = 1
    VIOLET = 2
    GREEN = 3

    PROFILE_PICTURE_CHOICES = (
        (str(BLUE), 'Blue-theme'),
        (str(RED), 'Red-theme'),
        (str(VIOLET), 'Violet-theme'),
        (str(GREEN), 'Green-theme'),
    )

    classroom_color = models.CharField(choices=PROFILE_PICTURE_CHOICES, max_length=10, default=str(BLUE))

    def __str__(self):
        return self.title


class Student(models.Model):
    students = models.ManyToManyField(User)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Students in {self.classroom.title}"
