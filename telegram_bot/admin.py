from django.contrib import admin
from .models import TelegramProfile


@admin.register(TelegramProfile)
class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "telegram_id",
        "chat_id",
        "username",
        "first_name",
        "current_session",
        "current_template_name",
        "registration_step",
        "pending_email",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_display_links = ("id", "telegram_id", "username")

    search_fields = (
        "telegram_id",
        "chat_id",
        "username",
        "first_name",
        "pending_email",
        "user__email",
    )

    list_filter = (
        "is_active",
        "registration_step",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "telegram_id",
        "chat_id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Telegram данные", {
            "fields": (
                "telegram_id",
                "chat_id",
                "username",
                "first_name",
                "is_active",
            )
        }),
        ("Связь с пользователем сайта", {
            "fields": (
                "user",
            )
        }),
        ("Чат и документы", {
            "fields": (
                "current_session",
                "current_template_name",
            )
        }),
        ("Регистрация через Telegram", {
            "fields": (
                "registration_step",
                "pending_email",
                "pending_password",
            )
        }),
        ("Системные даты", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )