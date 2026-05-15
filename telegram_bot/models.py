from django.db import models
from django.conf import settings

class TelegramProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="telegram_profile",
        null=True,
        blank=True
    )

    telegram_id = models.BigIntegerField(unique=True)
    chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    current_template_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    current_session = models.ForeignKey(
        "chats.ChatSession",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="telegram_profiles"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)