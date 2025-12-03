from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user",
        blank=True
    )
    first_name = models.CharField(max_length=50, verbose_name="Имя", blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phoneNumber = models.CharField(max_length=15, verbose_name="Номер телефона", blank=True)

    @property
    def role(self):
        return self.user.role

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.user.email
