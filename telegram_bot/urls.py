from django.urls import path
from .views import CreateTelegramLinkCodeView, TelegramWebhookView

app_name = "telegram_bot"
urlpatterns = [
    path("link-code/", CreateTelegramLinkCodeView.as_view()),
    path("webhook/", TelegramWebhookView.as_view()),
]
