# admin.py

from django.contrib import admin
from django.utils.html import format_html

from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0

    fields = (
        "role",
        "short_content",
        "created_at",
    )

    readonly_fields = (
        "role",
        "short_content",
        "created_at",
    )

    can_delete = False
    show_change_link = True

    def short_content(self, obj):
        if len(obj.content) > 100:
            return obj.content[:100] + "..."
        return obj.content

    short_content.short_description = "Сообщение"


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "messages_count",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "user__username",
        "user__email",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    inlines = [ChatMessageInline]

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "user",
                    "title",
                )
            }
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )

    def messages_count(self, obj):
        return obj.messages.count()

    messages_count.short_description = "Количество сообщений"


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "session",
        "user",
        "role",
        "short_content",
        "created_at",
    )

    list_filter = (
        "role",
        "created_at",
    )

    search_fields = (
        "content",
        "session__title",
        "session__user__username",
        "session__user__email",
    )

    readonly_fields = (
        "created_at",
        "formatted_content",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Информация о сообщении",
            {
                "fields": (
                    "session",
                    "role",
                    "formatted_content",
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

    def user(self, obj):
        return obj.session.user

    user.short_description = "Пользователь"

    def short_content(self, obj):
        if len(obj.content) > 80:
            return obj.content[:80] + "..."
        return obj.content

    short_content.short_description = "Сообщение"

    def formatted_content(self, obj):
        return format_html(
            "<div style='white-space: pre-wrap; max-width: 900px;'>{}</div>",
            obj.content
        )

    formatted_content.short_description = "Полный текст"