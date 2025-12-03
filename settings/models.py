from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class Settings(models.Model):
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Тёмная'),
        ('system', 'Системная'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ru', 'Русский'),
        ('kk', 'Қазақша'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='system')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')

    def __str__(self):
        return f"Настройки пользователя {self.user.username}"
