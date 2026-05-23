from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from chats.models import ChatSession
import requests
from users.models import Users
from .models import TelegramProfile
import traceback
import json
from ai_documents.services.documents import (
    DOCUMENT_TYPES,
    get_document,
    get_documents_list,
)
from ai_documents.services.generator_client import send_to_generator
from subscriptions.services.usage_limits import consume_user_token
from chats.models import ChatSession, ChatMessage
from django.contrib.auth import authenticate

def json_to_telegram_text(data):
    return json.dumps(data, ensure_ascii=False, indent=2)



@method_decorator(csrf_exempt, name="dispatch")
class TelegramWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    STATE_LOGIN_EMAIL = "login_email"
    STATE_LOGIN_PASSWORD = "login_password"

    STATE_REGISTER_EMAIL = "register_email"
    STATE_REGISTER_PASSWORD = "register_password"
    STATE_REGISTER_PASSWORD_CONFIRM = "register_password_confirm"

    def post(self, request):

        update = request.data

        if not isinstance(update, dict):
            return JsonResponse({"ok": True})

        message = update.get("message")

        if not isinstance(message, dict):
            return JsonResponse({"ok": True})

        text = message.get("text", "").strip()

        chat = message.get("chat") or {}
        from_user = message.get("from") or {}

        if not isinstance(chat, dict):
            return JsonResponse({"ok": True})

        if not isinstance(from_user, dict):
            return JsonResponse({"ok": True})

        chat_id = chat.get("id")
        telegram_id = from_user.get("id")
        username = from_user.get("username")
        first_name = from_user.get("first_name")

        if not chat_id or not telegram_id:
            return JsonResponse({"ok": True})
        update = request.data

        if not isinstance(update, dict):
            return JsonResponse({"ok": True})

        message = update.get("message")

        if not isinstance(message, dict):
            return JsonResponse({"ok": True})

        text = message.get("text", "").strip()

        chat = message.get("chat") or {}
        from_user = message.get("from") or {}

        if not isinstance(chat, dict) or not isinstance(from_user, dict):
            return JsonResponse({"ok": True})

        chat_id = chat.get("id")
        telegram_id = from_user.get("id")
        username = from_user.get("username")
        first_name = from_user.get("first_name")

        if not chat_id or not telegram_id:
            return JsonResponse({"ok": True})

        tg_profile, created = TelegramProfile.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "chat_id": chat_id,
                "username": username,
                "first_name": first_name,
            },
        )

        if tg_profile.chat_id != chat_id:
            tg_profile.chat_id = chat_id
            tg_profile.save(update_fields=["chat_id", "updated_at"])

        if text == "/start":
            if tg_profile.user:
                return JsonResponse({"ok": True})

            return JsonResponse({"ok": True})
        
        if text == "/login":
            tg_profile.registration_step = "login_email"
            tg_profile.save(update_fields=["registration_step", "updated_at"])

            return JsonResponse({"ok": True})
        
        if text == "/register":
            tg_profile.registration_step = "register_email"
            tg_profile.save(update_fields=["registration_step", "updated_at"])


            return JsonResponse({"ok": True})
        
        if tg_profile.registration_step == "register_email":
            email = text.lower().strip()

            if Users.objects.filter(email=email).exists():
                return JsonResponse({"ok": True})

            tg_profile.pending_email = email
            tg_profile.registration_step = "register_password"
            tg_profile.save(update_fields=["pending_email", "registration_step", "updated_at"])

            return JsonResponse({"ok": True})
        
        if tg_profile.registration_step == "register_password":
            password = text.strip()

            if len(password) < 8:
                return JsonResponse({"ok": True})

            tg_profile.pending_password = password
            tg_profile.registration_step = "register_password_confirm"
            tg_profile.save(update_fields=["pending_password", "registration_step", "updated_at"])

            return JsonResponse({"ok": True})
        if tg_profile.registration_step == "register_password_confirm":
            password_confirm = text.strip()

            if tg_profile.pending_password != password_confirm:
                tg_profile.pending_password = None
                tg_profile.registration_step = "register_password"
                tg_profile.save(update_fields=["pending_password", "registration_step", "updated_at"])

                return JsonResponse({"ok": True})

            user = Users.objects.create_user(
                email=tg_profile.pending_email,
                password=tg_profile.pending_password,
                agreementAccepted=True,
                privacyPolicyAccepted=True
            )

            tg_profile.user = user
            tg_profile.registration_step = None
            tg_profile.pending_email = None
            tg_profile.pending_password = None
            tg_profile.username = username
            tg_profile.first_name = first_name

            tg_profile.save(
                update_fields=[
                    "user",
                    "registration_step",
                    "pending_email",
                    "pending_password",
                    "username",
                    "first_name",
                    "updated_at",
                ]
            )

            return JsonResponse({"ok": True})
        if tg_profile.registration_step == "login_email":
            email = text.lower().strip()

            user = Users.objects.filter(email=email).first()

            if not user:
                return JsonResponse({"ok": True})

            existing_tg = TelegramProfile.objects.filter(user=user).exclude(id=tg_profile.id).first()

            if existing_tg:
                return JsonResponse({"ok": True})

            tg_profile.pending_email = email
            tg_profile.registration_step = "login_password"
            tg_profile.save(update_fields=["pending_email", "registration_step", "updated_at"])

            return JsonResponse({"ok": True})
        
        if tg_profile.registration_step == "login_password":
            password = text.strip()
            email = tg_profile.pending_email

            if not email:
                tg_profile.registration_step = "login_email"
                tg_profile.save(update_fields=["registration_step", "updated_at"])

                return JsonResponse({"ok": True})

            user = authenticate(
                request=request,
                username=email,
                password=password
            )

            if not user:

                return JsonResponse({"ok": True})

            existing_tg = TelegramProfile.objects.filter(user=user).exclude(id=tg_profile.id).first()

            if existing_tg:

                return JsonResponse({"ok": True})

            tg_profile.user = user
            tg_profile.registration_step = None
            tg_profile.pending_email = None
            tg_profile.username = username
            tg_profile.first_name = first_name

            tg_profile.save(
                update_fields=[
                    "user",
                    "registration_step",
                    "pending_email",
                    "username",
                    "first_name",
                    "updated_at",
                ]
            )

            return JsonResponse({"ok": True})

        if not tg_profile.user:
            return JsonResponse({"ok": True})
                
        if text == "/help":
            return JsonResponse({"ok": True})

        if text == "/profile":
            return JsonResponse({"ok": True})

        if text == "/new":
            session = ChatSession.objects.create(
                user=tg_profile.user, title="Telegram chat"
            )

            tg_profile.current_session = session
            tg_profile.save(update_fields=["current_session", "updated_at"])

            return JsonResponse({"ok": True})

        if text.startswith("/ask "):
            question = text.replace("/ask ", "", 1).strip()

            if not question:
                return JsonResponse({"ok": True})

            answer = handle_ai_question_from_telegram(
                tg_profile=tg_profile, question=question
            )

            return JsonResponse({"ok": True})

        if text.startswith("/price "):
            question = text.replace("/price ", "", 1).strip()

            answer = handle_price_question(tg_profile=tg_profile, question=question)

            return JsonResponse({"ok": True})

        if text.startswith("/winchance "):
            question = text.replace("/winchance ", "", 1).strip()

            answer = handle_win_chance_question(
                tg_profile=tg_profile, question=question
            )

            return JsonResponse({"ok": True})
        if text.startswith("/toplawyers "):
            question = text.replace("/toplawyers ", "", 1).strip()

            if not question:
                return JsonResponse({"ok": True})

            answer = handle_top_lawyers_question(
                tg_profile=tg_profile,
                question=question
            )

            return JsonResponse({"ok": True})
        if text == "/docs":
            documents = get_documents_list()

            message = "Доступные документы:\n\n"

            for doc in documents:
                message += f"• {doc.get('title')}\n"

            message += "\nЧтобы выбрать документ, напишите:\n/doc название документа"

            return JsonResponse({"ok": True})

        if text.startswith("/doc "):
            document_query = text.replace("/doc ", "", 1).strip()

            answer = handle_telegram_document_select(
                tg_profile=tg_profile, document_query=document_query
            )

            return JsonResponse({"ok": True})

        if text.startswith("/generate "):
            raw_json = text.replace("/generate ", "", 1).strip()

            answer = handle_telegram_document_generate(
                tg_profile=tg_profile, raw_json=raw_json
            )

            return JsonResponse({"ok": True})

        return JsonResponse({"ok": True})


from chats.models import ChatSession, ChatMessage
from subscriptions.services.usage_limits import consume_user_token


def handle_ai_question_from_telegram(tg_profile, question):
    try:
        session = get_or_create_telegram_session(tg_profile)

        user = tg_profile.user

        limit_response = consume_user_token(user)

        if limit_response:
            return "У вас закончились бесплатные запросы."

        ChatMessage.objects.create(session=session, role="user", content=question)

        payload = {"question": question, "session_id": session.id}

        r = requests.post(
            "https://etha-hypercatalectic-rueben.ngrok-free.dev/ask",
            json=payload,
            timeout=120,
        )

        r.raise_for_status()

        data = r.json()

        telegram_answer = json_to_telegram_text(data)

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=telegram_answer
        )

        return telegram_answer

    except Exception as e:
        traceback.print_exc()

        return "Ошибка при обращении к ИИ."


def get_or_create_telegram_session(tg_profile):

    if tg_profile.current_session:
        return tg_profile.current_session

    session = ChatSession.objects.create(user=tg_profile.user, title="Telegram chat")

    tg_profile.current_session = session
    tg_profile.save(update_fields=["current_session", "updated_at"])

    return session


def handle_price_question(tg_profile, question):
    try:
        session = get_or_create_telegram_session(tg_profile)
        user = tg_profile.user

        limit_response = consume_user_token(user)

        if limit_response:
            return "У вас закончились бесплатные запросы."

        ChatMessage.objects.create(session=session, role="user", content=question)

        r = requests.post(
            "https://etha-hypercatalectic-rueben.ngrok-free.dev/price",
            json={"question": question, "session_id": session.id},
            timeout=120,
        )

        r.raise_for_status()

        data = r.json()

        telegram_answer = json_to_telegram_text(data)

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=telegram_answer
        )

        return telegram_answer

    except Exception as e:
        return "Ошибка при расчёте стоимости дела."


def handle_win_chance_question(tg_profile, question):
    try:
        session = get_or_create_telegram_session(tg_profile)
        user = tg_profile.user

        limit_response = consume_user_token(user)

        if limit_response:
            return "У вас закончились бесплатные запросы."

        ChatMessage.objects.create(session=session, role="user", content=question)

        r = requests.post(
            "https://etha-hypercatalectic-rueben.ngrok-free.dev/article-win-chance",
            json={"question": question, "session_id": session.id},
            timeout=120,
        )

        r.raise_for_status()

        data = r.json()

        telegram_answer = json_to_telegram_text(data)

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=telegram_answer
        )

        return telegram_answer

    except Exception as e:
        return "Ошибка при анализе шансов."


def handle_telegram_document_select(tg_profile, document_query):
    session = get_or_create_telegram_session(tg_profile)

    found_template = None

    for template_name, document in DOCUMENT_TYPES.items():
        title = document.get("title", "")

        if (
            document_query.lower() in title.lower()
            or document_query.lower() in template_name.lower()
        ):
            found_template = template_name
            break

    if not found_template:
        return "Документ не найден. Напишите /docs, чтобы посмотреть список документов."

    document = get_document(found_template)

    fields_text = ""

    for field in document["fields"]:
        required = "обязательное" if field.get("required") else "необязательное"
        fields_text += (
            f"\n• {field['key']} — {field.get('label', field['key'])} ({required})"
        )

    tg_profile.current_template_name = found_template
    tg_profile.save(update_fields=["current_template_name", "updated_at"])

    response_data = {
        "type": "document_selected",
        "template_name": found_template,
        "title": document["title"],
        "fields": document["fields"],
        "message": "Документ выбран. Заполните поля и отправьте /generate JSON."
    }

    telegram_answer = json_to_telegram_text(response_data)

    ChatMessage.objects.create(
        session=session,
        role="assistant",
        content=telegram_answer
    )

    return telegram_answer


def handle_telegram_document_generate(tg_profile, raw_json):
    try:
        session = get_or_create_telegram_session(tg_profile)
        user = tg_profile.user

        template_name = tg_profile.current_template_name

        if not template_name:
            return "Сначала выберите документ через /doc название документа."

        if template_name not in DOCUMENT_TYPES:
            return "Выбранный документ больше не найден. Выберите заново через /docs."

        try:
            values = json.loads(raw_json)
        except json.JSONDecodeError:
            return (
                'Ошибка JSON. Отправьте данные в формате: /generate {"field": "value"}'
            )

        if not isinstance(values, dict):
            return "После /generate должен быть JSON-объект."

        document = get_document(template_name)

        required_keys = [
            field["key"] for field in document["fields"] if field.get("required")
        ]

        missing = [key for key in required_keys if not values.get(key)]

        if missing:
            return "Заполнены не все обязательные поля:\n\n" + "\n".join(
                [f"• {key}" for key in missing]
            )

        limit_response = consume_user_token(user)
        if limit_response:
            return "У вас закончились бесплатные запросы."

        ChatMessage.objects.create(
            session=session, role="user", content=f"Создание документа: {template_name}"
        )

        generator_response = send_to_generator(
            template_name=template_name, values=values
        )

        if generator_response.get("error"):
            return "Ошибка при создании документа."



        telegram_answer = json_to_telegram_text(generator_response)

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=telegram_answer
        )

        return telegram_answer
            
    except Exception as e:
        return "Ошибка при создании документа."

def handle_top_lawyers_question(tg_profile, question):
    try:
        session = get_or_create_telegram_session(tg_profile)
        user = tg_profile.user

        limit_response = consume_user_token(user)

        if limit_response:
            return "У вас закончились бесплатные запросы."

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        r = requests.post(
            "https://etha-hypercatalectic-rueben.ngrok-free.dev/top-lawyers-by-article",
            json={
                "question": question,
                "top_n": 5,
                "session_id": session.id
            },
            timeout=120,
        )

        r.raise_for_status()

        data = r.json()

        telegram_answer = json_to_telegram_text(data)

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=telegram_answer
        )

        return telegram_answer

    except Exception as e:
        return "Ошибка при поиске топ адвокатов."