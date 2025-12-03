from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Subscription(models.Model):
    PLAN_CHOICES = (
        ('1m', '1 месяц'),
        ('6m', '6 месяцев'),
        ('1y', '1 год'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="пользователь"
    )
    plan = models.CharField(max_length=2, choices=PLAN_CHOICES, verbose_name="тариф")
    

    start_date = models.DateTimeField(default=timezone.now, verbose_name="начало подписки")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="окончание подписки")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
  
        if not self.end_date and self.plan:
            if self.plan == '1m':
                self.end_date = self.start_date + timedelta(minutes=1)
            elif self.plan == '6m':
                self.end_date = self.start_date + timedelta(days=180)
            elif self.plan == '1y':
                self.end_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)
    @property
    def is_active(self):
        return self.end_date > timezone.now()

    def __str__(self):
        return f"{self.user.email} ({self.plan}) с {self.start_date.date()} по {self.end_date.date()}"
