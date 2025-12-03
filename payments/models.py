from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class Payment(models.Model):
    PURPOSE_CHOICES = [
        ("invoice", "Invoice"),
        ("subscription", "Subscription"),
    ]

    payer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments_made',
        verbose_name='Плательщик'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments_received',
        verbose_name='Получатель',
        null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_id = models.PositiveIntegerField(unique=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    purpose = models.CharField(
        max_length=20,
        choices=PURPOSE_CHOICES,
        default="invoice"
    )
    plan = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return f"{self.payer} → {self.receiver or 'Service'} | {self.amount} ({self.purpose})"
