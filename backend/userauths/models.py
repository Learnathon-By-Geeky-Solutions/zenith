from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Create your models here.

class User(AbstractUser):
    ''' Custom User Model '''

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, blank=True, null=True)
    refresh_token = models.CharField(max_length=1000, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        email_username, full_name = self.email.split('@')

        if self.full_name == '' or self.full_name == None:
            self.full_name = email_username
        if self.username == '' or self.username == None:
            self.username = email_username

        super(User, self).save(*args, **kwargs)

class Profile(models.Model):
    ''' User Profile Model '''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='user_folder', default='default-user.jpg', blank=True, null=True)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)

    def save(self, *args, **kwargs):
        if self.full_name == '' or self.full_name == None:
            self.full_name = self.user.username

        super(Profile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Signals to create and save user profile
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)