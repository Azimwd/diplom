# admin.py

from django.contrib import admin
from django.utils.html import format_html

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice_id",
        "payer",
        "receiver",
        "amount",
        "purpose",
        "plan",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "is_paid",
        "purpose",
        "plan",
        "created_at",
    )

    search_fields = (
        "invoice_id",
        "payer__username",
        "payer__email",
        "receiver__username",
        "receiver__email",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "payer",
        "receiver",
    )

    fieldsets = (
        (
            "Информация о платеже",
            {
                "fields": (
                    "invoice_id",
                    "amount",
                    "purpose",
                    "plan",
                    "is_paid",
                )
            }
        ),
        (
            "Участники платежа",
            {
                "fields": (
                    "payer",
                    "receiver",
                )
            }
        ),
        (
            "Системная информация",
            {
                "fields": (
                    "created_at",
                )
            }
        ),
    )

    def payment_status(self, obj):
        if obj.is_paid:
            return format_html(
                "<span style='color: green; font-weight: bold;'>Оплачено</span>"
            )

        return format_html(
            "<span style='color: red; font-weight: bold;'>Не оплачено</span>"
        )

    payment_status.short_description = "Статус"