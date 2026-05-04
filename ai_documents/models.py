from django.conf import settings
from django.db import models


class AiDocumentDialog(models.Model):
    STATE_DOCUMENT_DETECTION = "document_detection"
    STATE_CONFIRMATION = "confirmation"
    STATE_DOCUMENT_SELECTION = "document_selection"
    STATE_FIELD_COLLECTION = "field_collection"
    STATE_GENERATION = "generation"

    STATE_CHOICES = [
        (STATE_DOCUMENT_DETECTION, "Определение документа"),
        (STATE_CONFIRMATION, "Подтверждение"),
        (STATE_DOCUMENT_SELECTION, "Выбор документа"),
        (STATE_FIELD_COLLECTION, "Заполнение полей"),
        (STATE_GENERATION, "Генерация"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_document_dialog"
    )

    state = models.CharField(
        max_length=50,
        choices=STATE_CHOICES,
        default=STATE_DOCUMENT_DETECTION
    )

    template_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    values = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)