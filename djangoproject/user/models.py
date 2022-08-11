from cProfile import Profile
from distutils.command.upload import upload
from email.mime import image
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    bio = models.TextField(max_length=200)
    passport = models.ImageField(default='passport.jpg', upload_to='image')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
       return f'{self.user.username} profile' 