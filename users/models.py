from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.contrib.auth.models import AbstractUser
from django.conf import settings

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