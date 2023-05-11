from django.contrib import admin

from .models import PasswordResetLink, SubMails, UserProfile

# Register your models here.
admin.site.register(PasswordResetLink)
admin.site.register(SubMails)
admin.site.register(UserProfile)