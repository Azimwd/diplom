# admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "plan",
        "subscription_status",
        "start_date",
        "end_date",
        "created_at",
    )

    list_filter = (
        "plan",
        "start_date",
        "end_date",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "created_at",
        "subscription_status",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
    )

    fieldsets = (
        (
            "Информация о подписке",
            {
                "fields": (
                    "user",
                    "plan",
                    "subscription_status",
                )
            }
        ),
        (
            "Срок действия",
            {
                "fields": (
                    "start_date",
                    "end_date",
                )
            }
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "created_at",
                )
            }
        ),
    )

    def subscription_status(self, obj):
        if obj.end_date and obj.end_date > timezone.now():
            return format_html(
                "<span style='color: green; font-weight: bold;'>Активна</span>"
            )

        return format_html(
            "<span style='color: red; font-weight: bold;'>Истекла</span>"
        )

    subscription_status.short_description = "Статус"