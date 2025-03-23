from django.contrib import admin
from .models import Assignment, AssignmentStatus

# Register your models here.

admin.site.register(Assignment)
admin.site.register(AssignmentStatus)
