from django.contrib import admin
from userauths.models import User, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'date']

#we need register our models
admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)

