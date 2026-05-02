from django.contrib import admin
from django.utils import timezone
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "plan",
        "start_date",
        "end_date",
        "active_status",
        "created_at",
    )

    list_filter = (
        "plan",
        "start_date",
        "end_date",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__id",
    )

    readonly_fields = (
        "created_at",
        "active_status",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "user",
                "plan",
            )
        }),
        ("Срок подписки", {
            "fields": (
                "start_date",
                "end_date",
                "active_status",
            )
        }),
        ("Системная информация", {
            "fields": (
                "created_at",
            )
        }),
    )

    @admin.display(description="Активна")
    def active_status(self, obj):
        if obj.end_date and obj.end_date > timezone.now():
            return "Да"
        return "Нет"