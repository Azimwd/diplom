from django.contrib import admin
from django.utils.html import format_html
import json

from .models import AiDocumentDialog


@admin.register(AiDocumentDialog)
class AiDocumentDialogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "state",
        "template_name",
        "short_values",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "state",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "template_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "formatted_values",
    )

    ordering = (
        "-updated_at",
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
            "Состояние диалога",
            {
                "fields": (
                    "state",
                    "template_name",
                )
            }
        ),
        (
            "Данные документа",
            {
                "fields": (
                    "values",
                    "formatted_values",
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

    def short_values(self, obj):
        if not obj.values:
            return "-"

        text = json.dumps(obj.values, ensure_ascii=False)

        if len(text) > 80:
            return text[:80] + "..."

        return text

    short_values.short_description = "Данные"

    def formatted_values(self, obj):
        if not obj.values:
            return "-"

        pretty_json = json.dumps(
            obj.values,
            ensure_ascii=False,
            indent=4
        )

        return format_html(
            "<pre style='white-space: pre-wrap;'>{}</pre>",
            pretty_json
        )

    formatted_values.short_description = "Данные в JSON"