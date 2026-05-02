from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TelegramLinkCode
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from .models import TelegramLinkCode, TelegramProfile

class CreateTelegramLinkCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        link_code = TelegramLinkCode.generate_for_user(request.user)

        return Response({
            "code": link_code.code,
            "message": "Отправьте этот код Telegram-боту"
        })
    

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })


@method_decorator(csrf_exempt, name="dispatch")
class TelegramWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        update = request.data

        message = update.get("message", {})
        text = message.get("text", "")
        chat = message.get("chat", {})
        from_user = message.get("from", {})

        chat_id = chat.get("id")
        telegram_id = from_user.get("id")
        username = from_user.get("username")

        if not chat_id or not telegram_id:
            return JsonResponse({"ok": True})

        if text == "/start":
            send_telegram_message(
                chat_id,
                "Здравствуйте. Для привязки аккаунта отправьте код с сайта."
            )
            return JsonResponse({"ok": True})

        link_code = TelegramLinkCode.objects.filter(code=text.strip()).first()

        if link_code:
            if link_code.is_expired():
                send_telegram_message(chat_id, "Код истёк. Создайте новый код на сайте.")
                return JsonResponse({"ok": True})

            TelegramProfile.objects.update_or_create(
                user=link_code.user,
                defaults={
                    "telegram_id": telegram_id,
                    "chat_id": chat_id,
                    "username": username,
                }
            )

            link_code.delete()

            send_telegram_message(chat_id, "Telegram успешно привязан к вашему аккаунту.")
            return JsonResponse({"ok": True})

        tg_profile = TelegramProfile.objects.filter(telegram_id=telegram_id).first()

        if not tg_profile:
            send_telegram_message(
                chat_id,
                "Аккаунт не привязан. Сначала получите код на сайте."
            )
            return JsonResponse({"ok": True})

        user = tg_profile.user

        answer = f"Ваш аккаунт найден: {user.email}. Сообщение: {text}"

        send_telegram_message(chat_id, answer)

        return JsonResponse({"ok": True})