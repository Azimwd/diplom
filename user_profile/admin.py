# admin.py

from django.contrib import admin
from django.utils.html import format_html

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "avatar_preview",
        "user",
        "full_name",
        "phoneNumber",
        "role",
    )

    search_fields = (
        "user__email",
        "user__username",
        "first_name",
        "last_name",
        "phoneNumber",
    )

    readonly_fields = (
        "avatar_preview_large",
        "role",
    )

    ordering = (
        "id",
    )

    list_select_related = (
        "user",
    )

    fieldsets = (
        (
            "Пользователь",
            {
                "fields": (
                    "user",
                    "role",
                )
            }
        ),
        (
            "Личная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phoneNumber",
                )
            }
        ),
        (
            "Аватар",
            {
                "fields": (
                    "avatar",
                    "avatar_preview_large",
                )
            }
        ),
    )

    def full_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()

        return full_name or "-"

    full_name.short_description = "ФИО"

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                "<img src='{}' width='40' height='40' style='border-radius:50%; object-fit:cover;' />",
                obj.avatar.url
            )

        return "-"

    avatar_preview.short_description = "Аватар"

    def avatar_preview_large(self, obj):
        if obj.avatar:
            return format_html(
                "<img src='{}' width='120' style='border-radius:10px;' />",
                obj.avatar.url
            )

        return "Аватар отсутствует"

    avatar_preview_large.short_description = "Предпросмотр"