from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    CHOICES = (
        ('HOD', 'HOD'),
        ('STUDENT', 'STUDENT'),
        ('TEACHER', 'TEACHER')
    )

    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=30, choices=CHOICES)
    photo = models.ImageField(upload_to='media/profile_pic', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
