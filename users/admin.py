# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Users, RefreshTokenStorage


class RefreshTokenInline(admin.TabularInline):
    model = RefreshTokenStorage
    extra = 0

    fields = (
        "short_token",
        "userAgent",
        "created",
    )

    readonly_fields = (
        "short_token",
        "userAgent",
        "created",
    )

    can_delete = True
    show_change_link = True

    def short_token(self, obj):
        if len(obj.refreshToken) > 50:
            return obj.refreshToken[:50] + "..."
        return obj.refreshToken

    short_token.short_description = "Refresh Token"


@admin.register(Users)
class UsersAdmin(UserAdmin):
    model = Users

    list_display = (
        "id",
        "email",
        "role",
        "freeRequest",
        "agreementAccepted",
        "privacyPolicyAccepted",
        "is_staff",
        "is_active",
        "createdAt",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
        "agreementAccepted",
        "privacyPolicyAccepted",
        "createdAt",
    )

    search_fields = (
        "email",
    )

    ordering = (
        "-createdAt",
    )

    readonly_fields = (
        "createdAt",
        "last_login",
    )

    inlines = [RefreshTokenInline]

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "email",
                    "password",
                )
            }
        ),
        (
            "Роль и лимиты",
            {
                "fields": (
                    "role",
                    "freeRequest",
                )
            }
        ),
        (
            "Согласия",
            {
                "fields": (
                    "agreementAccepted",
                    "privacyPolicyAccepted",
                    "agreementVersion",
                )
            }
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            }
        ),
        (
            "Системная информация",
            {
                "fields": (
                    "last_login",
                    "createdAt",
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "role",
                    "freeRequest",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )


@admin.register(RefreshTokenStorage)
class RefreshTokenStorageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "short_token",
        "short_user_agent",
        "created",
    )

    search_fields = (
        "user__email",
        "userAgent",
    )

    readonly_fields = (
        "created",
        "formatted_token",
    )

    ordering = (
        "-created",
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
                )
            }
        ),
        (
            "Refresh token",
            {
                "fields": (
                    "formatted_token",
                    "userAgent",
                )
            }
        ),
        (
            "Системная информация",
            {
                "fields": (
                    "created",
                )
            }
        ),
    )

    def short_token(self, obj):
        if len(obj.refreshToken) > 40:
            return obj.refreshToken[:40] + "..."
        return obj.refreshToken

    short_token.short_description = "Token"

    def short_user_agent(self, obj):
        if not obj.userAgent:
            return "-"

        if len(obj.userAgent) > 60:
            return obj.userAgent[:60] + "..."

        return obj.userAgent

    short_user_agent.short_description = "User-Agent"

    def formatted_token(self, obj):
        return format_html(
            "<div style='max-width:900px; word-break:break-all;'>{}</div>",
            obj.refreshToken
        )

    formatted_token.short_description = "Полный token"