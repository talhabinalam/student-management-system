from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

class CustomUser(AbstractUser):
    CHOICES = (
        ('HOD', 'HOD'),
        ('STUDENT', 'STUDENT'),
        ('TEACHER', 'TEACHER')
    )

    user_type = models.CharField(max_length=30, choices=CHOICES)
    photo = models.ImageField(upload_to='media/profile_pic')

