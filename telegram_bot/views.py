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


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    response = requests.post(
        url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    )


@method_decorator(csrf_exempt, name="dispatch")
class TelegramWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

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

        user, _ = Users.objects.get_or_create(
            email=f"tg_{telegram_id}@telegram.local",
            defaults={
                "first_name": first_name or "",
            },
        )

        tg_profile, created = TelegramProfile.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "user": user,
                "chat_id": chat_id,
                "username": username,
                "first_name": first_name,
            },
        )

        if tg_profile.chat_id != chat_id:
            tg_profile.chat_id = chat_id
            tg_profile.save(update_fields=["chat_id", "updated_at"])

        if text == "/start":
            send_telegram_message(
                chat_id,
                "Здравствуйте. Вы вошли через Telegram.\n\n"
                "Доступные команды:\n"
                "/help — список команд\n"
                "/ask текст — обычный ИИ\n"
                "/price текст — стоимость дела\n"
                "/winchance текст — шанс победы\n"
                "/toplawyers текст — топ адвокатов по статье\n"
                "/docs — список документов\n"
                "/doc название — выбрать документ\n"
                "/generate JSON — создать документ\n"
                "/new — новая сессия\n",
            )
            return JsonResponse({"ok": True})

        if text == "/help":
            send_telegram_message(
                chat_id,
                "Команды:\n\n"
                "/ask текст — обычный ИИ\n"
                "/price текст — стоимость дела\n"
                "/winchance текст — шанс победы\n"
                "/toplawyers текст — топ адвокатов по статье\n"
                "/docs — список документов\n"
                "/doc название — выбрать документ\n"
                "/generate JSON — создать документ\n"
                "/new — новая сессия\n",
            )
            return JsonResponse({"ok": True})

        if text == "/profile":
            send_telegram_message(
                chat_id,
                (
                    f"Ваш Telegram ID: {telegram_id}\n" f"Username: @{username}"
                    if username
                    else f"Ваш Telegram ID: {telegram_id}"
                ),
            )
            return JsonResponse({"ok": True})

        if text == "/new":
            session = ChatSession.objects.create(
                user=tg_profile.user, title="Telegram chat"
            )

            tg_profile.current_session = session
            tg_profile.save(update_fields=["current_session", "updated_at"])

            send_telegram_message(
                chat_id, "Создана новая сессия. Теперь можете задать новый вопрос."
            )
            return JsonResponse({"ok": True})

        if text.startswith("/ask "):
            question = text.replace("/ask ", "", 1).strip()

            if not question:
                send_telegram_message(chat_id, "Напишите вопрос после команды /ask")
                return JsonResponse({"ok": True})

            answer = handle_ai_question_from_telegram(
                tg_profile=tg_profile, question=question
            )

            send_telegram_message(chat_id, answer)
            return JsonResponse({"ok": True})

        if text.startswith("/price "):
            question = text.replace("/price ", "", 1).strip()

            answer = handle_price_question(tg_profile=tg_profile, question=question)

            send_telegram_message(chat_id, answer)

            return JsonResponse({"ok": True})

        if text.startswith("/winchance "):
            question = text.replace("/winchance ", "", 1).strip()

            answer = handle_win_chance_question(
                tg_profile=tg_profile, question=question
            )

            send_telegram_message(chat_id, answer)

            return JsonResponse({"ok": True})
        if text.startswith("/toplawyers "):
            question = text.replace("/toplawyers ", "", 1).strip()

            if not question:
                send_telegram_message(chat_id, "Напишите вопрос после команды /toplawyers")
                return JsonResponse({"ok": True})

            answer = handle_top_lawyers_question(
                tg_profile=tg_profile,
                question=question
            )

            send_telegram_message(chat_id, answer)
            return JsonResponse({"ok": True})
        if text == "/docs":
            documents = get_documents_list()

            message = "Доступные документы:\n\n"

            for doc in documents:
                message += f"• {doc.get('title')}\n"

            message += "\nЧтобы выбрать документ, напишите:\n/doc название документа"

            send_telegram_message(chat_id, message)
            return JsonResponse({"ok": True})

        if text.startswith("/doc "):
            document_query = text.replace("/doc ", "", 1).strip()

            answer = handle_telegram_document_select(
                tg_profile=tg_profile, document_query=document_query
            )

            send_telegram_message(chat_id, answer)
            return JsonResponse({"ok": True})

        if text.startswith("/generate "):
            raw_json = text.replace("/generate ", "", 1).strip()

            answer = handle_telegram_document_generate(
                tg_profile=tg_profile, raw_json=raw_json
            )

            send_telegram_message(chat_id, answer)
            return JsonResponse({"ok": True})

        send_telegram_message(
            chat_id,
            "Я вас понял. Чтобы задать вопрос ИИ, напишите:\n\n" "/ask ваш вопрос",
        )

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

        answer = data.get("answer") or "ИИ не вернул ответ."

        ChatMessage.objects.create(session=session, role="assistant", content=answer)

        return answer

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

        answer = data.get("answer", "Нет ответа от ИИ")

        ChatMessage.objects.create(session=session, role="assistant", content=answer)

        return answer

    except Exception as e:
        print("PRICE ERROR:", e)
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

        answer = data.get("answer", "Нет ответа от ИИ")

        stats = (
            f"\n\n"
            f"Статья: {data.get('article')}\n"
            f"Всего дел: {data.get('total')}\n"
            f"Побед: {data.get('wins')}\n"
            f"Поражений: {data.get('losses')}\n"
            f"Шанс победы: {data.get('win_rate')}%"
        )

        final_answer = answer + stats

        ChatMessage.objects.create(
            session=session, role="assistant", content=final_answer
        )

        return final_answer

    except Exception as e:
        print("WIN CHANCE ERROR:", e)
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

    ChatMessage.objects.create(
        session=session,
        role="assistant",
        content=f"Выбран документ: {document['title']}",
    )

    return (
        f"Выбран документ: {document['title']}\n\n"
        f"Нужно заполнить поля:\n"
        f"{fields_text}\n\n"
        f"Теперь отправьте данные так:\n\n"
        f'/generate {{"field_key": "значение"}}'
    )


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

        response_data = generator_response.get("response", {})

        file_url = (
            response_data.get("file_url")
            or response_data.get("download_url")
            or response_data.get("url")
        )

        if not file_url:
            return "Документ создан, но ссылка на файл не вернулась."

        ChatMessage.objects.create(
            session=session, role="assistant", content=f"Документ создан: {file_url}"
        )

        return f"Документ успешно создан:\n{file_url}"

    except Exception as e:
        print("DOCUMENT GENERATE ERROR:", e)
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

        answer = data.get("answer", "Нет ответа от ИИ")

        content_data = {
            "type": "top_lawyers_by_article",
            "intent": data.get("intent"),
            "found": data.get("found"),
            "answer": answer,

            "article": data.get("article"),
            "requested_article": data.get("requested_article"),
            "total_lawyers": data.get("total_lawyers"),
            "lawyers": data.get("lawyers", []),

            "detector_source": data.get("detector_source"),
            "confidence": data.get("confidence"),

            "session_id": session.id,
        }

        content_json = json.dumps(content_data, ensure_ascii=False)

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=content_json
        )

        return answer

    except Exception as e:
        print("TOP LAWYERS ERROR:", e)
        return "Ошибка при поиске топ адвокатов."