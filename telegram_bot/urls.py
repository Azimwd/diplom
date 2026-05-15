# telegram_bot/urls.py

from django.urls import path
from .views import TelegramWebhookView

app_name = "telegram-bot"

urlpatterns = [
    path("webhook/", TelegramWebhookView.as_view()),
]