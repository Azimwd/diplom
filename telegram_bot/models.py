from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone
from datetime import timedelta

class TelegramProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="telegram_profile"
    )
    telegram_id = models.BigIntegerField(unique=True)
    chat_id = models.BigIntegerField()
    username = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — {self.telegram_id}"


class TelegramLinkCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()

    @staticmethod
    def generate_for_user(user):
        code = str(uuid.uuid4())[:8].upper()

        return TelegramLinkCode.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

    def is_expired(self):
        return timezone.now() > self.expires_at