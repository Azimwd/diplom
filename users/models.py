from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
import uuid
from datetime import timedelta

class UsersManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
    
class Users(AbstractUser):
    username = None
    ROLE_CHOICES = [
        ('user', 'пользователь'),
    ]
    email = models.EmailField(unique=True, verbose_name="email")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name="role")
    agreementAccepted = models.BooleanField(default=False)
    privacyPolicyAccepted = models.BooleanField(default=False)
    agreementVersion = models.CharField(max_length=10, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    freeRequest = models.IntegerField(default=3, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UsersManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

class RefreshTokenStorage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='refresh_tokens')
    refreshToken = models.TextField()
    userAgent = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — {self.userAgent or 'unknown'}"
    

class RegistrationSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    email = models.EmailField()
    role = models.CharField(max_length=15, choices=Users.ROLE_CHOICES)
    password = models.CharField(max_length=128, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    last_email_sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} ({self.role})"


class SocialOnboardingSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=30, default="google")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @classmethod
    def create(cls, user, provider="google", ttl_minutes=10):
        return cls.objects.create(
            user=user,
            provider=provider,
            expires_at=timezone.now() + timedelta(minutes=ttl_minutes),
        )

    def is_expired(self):
        return timezone.now() >= self.expires_at