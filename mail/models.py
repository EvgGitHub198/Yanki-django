from django.db import models
from django.contrib.auth.models import User

class PasswordResetLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)



class SubMails(models.Model):
    email = models.CharField(max_length=70, unique=True)
    confirm_token = models.CharField(max_length=64)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(blank=True, null=True)  # Добавлено новое поле email
    phone = models.CharField(max_length=30)
    index = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
