from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Users,
    RefreshTokenStorage,
    RegistrationSession,
    SocialOnboardingSession,
)


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
        "is_active",
        "is_staff",
        "is_superuser",
        "createdAt",
    )

    list_display_links = ("id", "email")

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "agreementAccepted",
        "privacyPolicyAccepted",
        "createdAt",
    )

    ordering = ("-createdAt",)

    readonly_fields = (
        "createdAt",
        "last_login",
        "date_joined",
    )

    fieldsets = (
        ("Данные пользователя", {
            "fields": (
                "email",
                "password",
                "first_name",
                "last_name",
                "role",
                "freeRequest",
            )
        }),
        ("Согласия", {
            "fields": (
                "agreementAccepted",
                "privacyPolicyAccepted",
                "agreementVersion",
            )
        }),
        ("Права доступа", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Важные даты", {
            "fields": (
                "last_login",
                "date_joined",
                "createdAt",
            )
        }),
    )

    add_fieldsets = (
        ("Создание пользователя", {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "role",
                "freeRequest",
                "is_active",
                "is_staff",
                "is_superuser",
            ),
        }),
    )


@admin.register(RefreshTokenStorage)
class RefreshTokenStorageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "short_token",
        "userAgent",
        "created",
    )

    list_display_links = ("id", "user")

    search_fields = (
        "user__email",
        "refreshToken",
        "userAgent",
    )

    list_filter = (
        "created",
    )

    readonly_fields = (
        "user",
        "refreshToken",
        "userAgent",
        "created",
    )

    ordering = ("-created",)

    def short_token(self, obj):
        if not obj.refreshToken:
            return "-"
        return obj.refreshToken[:25] + "..."

    short_token.short_description = "Refresh token"


@admin.register(RegistrationSession)
class RegistrationSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "role",
        "is_email_verified",
        "last_email_sent_at",
    )

    list_display_links = ("id", "email")

    search_fields = (
        "email",
        "session_id",
        "email_verification_token",
    )

    list_filter = (
        "role",
        "is_email_verified",
        "last_email_sent_at",
    )

    readonly_fields = (
        "session_id",
        "email_verification_token",
    )

    ordering = ("-id",)


@admin.register(SocialOnboardingSession)
class SocialOnboardingSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "provider",
        "session_id",
        "created_at",
        "expires_at",
        "is_expired_display",
    )

    list_display_links = ("id", "user")

    search_fields = (
        "user__email",
        "provider",
        "session_id",
    )

    list_filter = (
        "provider",
        "created_at",
        "expires_at",
    )

    readonly_fields = (
        "session_id",
        "created_at",
    )

    ordering = ("-created_at",)

    def is_expired_display(self, obj):
        return obj.is_expired()

    is_expired_display.boolean = True
    is_expired_display.short_description = "Истёк"