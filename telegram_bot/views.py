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
from django.utils import timezone
from subscriptions.models import Subscription
from payments.services import (
    create_subscription_payment,
    build_robokassa_url,
    get_subscription_plans_for_response,
    SUBSCRIPTION_PLANS,
)

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
                return JsonResponse({
                    "ok": True,
                    "type": "start",
                    "authenticated": True,
                    "message": "Вы уже авторизованы."
                })

            return JsonResponse({
                "ok": True,
                "type": "start",
                "authenticated": False,
                "message": "Используйте /login для входа или /register для регистрации."
            })
                
        if text == "/login":
            tg_profile.registration_step = "login_email"
            tg_profile.save(update_fields=["registration_step", "updated_at"])

            return JsonResponse({
                "ok": True,
                "type": "login_started",
                "step": "login_email",
                "message": "Введите email."
            })
        
        if text == "/register":
            tg_profile.registration_step = "register_email"
            tg_profile.save(update_fields=["registration_step", "updated_at"])

            return JsonResponse({
                "ok": True,
                "type": "register_started",
                "step": "register_email",
                "message": "Введите email для регистрации."
            })
        
        if tg_profile.registration_step == "register_email":
            email = text.lower().strip()

            if Users.objects.filter(email=email).exists():
                return JsonResponse({
                    "ok": False,
                    "error": "email_already_exists",
                    "message": "Пользователь с таким email уже существует."
                })

            tg_profile.pending_email = email
            tg_profile.registration_step = "register_password"
            tg_profile.save(update_fields=["pending_email", "registration_step", "updated_at"])

            return JsonResponse({
                "ok": True,
                "type": "register_email_saved",
                "step": "register_password",
                "message": "Email сохранён. Введите пароль."
            })
        
        if tg_profile.registration_step == "register_password":
            password = text.strip()

            if len(password) < 8:
                return JsonResponse({
                    "ok": False,
                    "error": "password_too_short",
                    "message": "Пароль должен содержать минимум 8 символов."
                })

            tg_profile.pending_password = password
            tg_profile.registration_step = "register_password_confirm"
            tg_profile.save(update_fields=["pending_password", "registration_step", "updated_at"])

            return JsonResponse({
                "ok": True,
                "type": "register_password_saved",
                "step": "register_password_confirm",
                "message": "Повторите пароль."
            })
        
        if tg_profile.registration_step == "register_password_confirm":
            password_confirm = text.strip()

            if tg_profile.pending_password != password_confirm:
                tg_profile.pending_password = None
                tg_profile.registration_step = "register_password"
                tg_profile.save(update_fields=["pending_password", "registration_step", "updated_at"])

                return JsonResponse({
                    "ok": False,
                    "error": "passwords_do_not_match",
                    "step": "register_password",
                    "message": "Пароли не совпадают. Введите пароль заново."
                })

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

            return JsonResponse({
                "ok": True,
                "type": "register_completed",
                "message": "Регистрация завершена."
            })
        
        if tg_profile.registration_step == "login_email":
            email = text.lower().strip()

            user = Users.objects.filter(email=email).first()

            if not user:
                return JsonResponse({
                    "ok": False,
                    "error": "user_not_found",
                    "step": "login_email",
                    "message": "Пользователь с таким email не найден."
                })

            existing_tg = TelegramProfile.objects.filter(user=user).exclude(id=tg_profile.id).first()

            if existing_tg:
                return JsonResponse({
                    "ok": False,
                    "error": "telegram_already_linked",
                    "message": "Этот аккаунт уже привязан к другому Telegram-профилю."
                })

            tg_profile.pending_email = email
            tg_profile.registration_step = "login_password"
            tg_profile.save(update_fields=["pending_email", "registration_step", "updated_at"])

            return JsonResponse({
                "ok": True,
                "type": "login_email_saved",
                "step": "login_password",
                "message": "Email найден. Введите пароль."
            })
                
        if tg_profile.registration_step == "login_password":
            password = text.strip()
            email = tg_profile.pending_email

            if not email:
                tg_profile.registration_step = "login_email"
                tg_profile.save(update_fields=["registration_step", "updated_at"])

                return JsonResponse({
                    "ok": False,
                    "error": "missing_pending_email",
                    "step": "login_email",
                    "message": "Email не найден. Введите email заново."
                })

            user = authenticate(
                request=request,
                username=email,
                password=password
            )

            if not user:
                return JsonResponse({
                    "ok": False,
                    "error": "invalid_credentials",
                    "step": "login_password",
                    "message": "Неверный email или пароль."
                })

            existing_tg = TelegramProfile.objects.filter(user=user).exclude(id=tg_profile.id).first()

            if existing_tg:
                return JsonResponse({
                    "ok": False,
                    "error": "telegram_already_linked",
                    "message": "Этот аккаунт уже привязан к другому Telegram-профилю."
                })

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

            return JsonResponse({
                "ok": True,
                "type": "login_completed",
                "message": "Вход выполнен успешно."
            })

        if not tg_profile.user:
            return JsonResponse({
                "ok": False,
                "error": "not_authenticated",
                "message": "Сначала выполните вход через /login или регистрацию через /register."
            })
        
        if text == "/plans":
            answer = get_telegram_subscription_plans()
            return JsonResponse(answer, safe=False)

        if text.startswith("/subscribe"):
            parts = text.split()

            if len(parts) != 2:
                return JsonResponse({
                    "ok": False,
                    "error": "invalid_subscribe_command",
                    "message": "Используйте команду: /subscribe 1m, /subscribe 6m или /subscribe 1y"
                })

            plan = parts[1].strip()

            answer = create_telegram_subscription_invoice(
                tg_profile=tg_profile,
                plan=plan
            )

            return JsonResponse(answer, safe=False)

        if text == "/subscription":
            answer = get_telegram_subscription_status(tg_profile)
            return JsonResponse(answer, safe=False)    

        if text == "/new":
            session = ChatSession.objects.create(
                user=tg_profile.user,
                title="Telegram chat"
            )

            tg_profile.current_session = session
            tg_profile.save(update_fields=["current_session", "updated_at"])

            return JsonResponse({
                "ok": True,
                "type": "new_session_created",
                "session_id": session.id,
                "message": "Новая Telegram-сессия создана."
            })
        
        if text.startswith("/ask "):
            question = text.replace("/ask ", "", 1).strip()

            if not question:
                return JsonResponse({
                    "ok": False,
                    "error": "empty_question",
                    "message": "После /ask нужно написать вопрос."
                })

            answer = handle_ai_question_from_telegram(
                tg_profile=tg_profile,
                question=question
            )

            return JsonResponse(answer, safe=False)

        if text.startswith("/price "):
            question = text.replace("/price ", "", 1).strip()

            if not question:
                return JsonResponse({
                    "ok": False,
                    "error": "empty_question",
                    "message": "После /price нужно написать вопрос."
                })

            answer = handle_price_question(
                tg_profile=tg_profile,
                question=question
            )

            return JsonResponse(answer, safe=False)

        if text.startswith("/winchance "):
            question = text.replace("/winchance ", "", 1).strip()

            if not question:
                return JsonResponse({
                    "ok": False,
                    "error": "empty_question",
                    "message": "После /winchance нужно написать вопрос."
                })

            answer = handle_win_chance_question(
                tg_profile=tg_profile,
                question=question
            )

            return JsonResponse(answer, safe=False)

        if text.startswith("/toplawyers "):
            question = text.replace("/toplawyers ", "", 1).strip()

            if not question:
                return JsonResponse({
                    "ok": False,
                    "error": "empty_question",
                    "message": "После /toplawyers нужно написать вопрос."
                })

            answer = handle_top_lawyers_question(
                tg_profile=tg_profile,
                question=question
            )

            return JsonResponse(answer, safe=False)
        
        if text == "/docs":
            documents = get_documents_list()

            answer = {
                "ok": True,
                "type": "documents_list",
                "documents": documents,
                "message": "Доступные документы получены."
            }

            return JsonResponse(answer, safe=False)

        if text.startswith("/doc "):
            document_query = text.replace("/doc ", "", 1).strip()

            if not document_query:
                return JsonResponse({
                    "ok": False,
                    "error": "empty_document_query",
                    "message": "После /doc нужно указать название документа."
                })

            answer = handle_telegram_document_select(
                tg_profile=tg_profile,
                document_query=document_query
            )

            return JsonResponse(answer, safe=False)

        if text.startswith("/generate "):
            raw_json = text.replace("/generate ", "", 1).strip()

            if not raw_json:
                return JsonResponse({
                    "ok": False,
                    "error": "empty_generate_payload",
                    "message": "После /generate нужно передать JSON с данными документа."
                })

            answer = handle_telegram_document_generate(
                tg_profile=tg_profile,
                raw_json=raw_json
            )

            return JsonResponse(answer, safe=False)

        return JsonResponse({
            "ok": False,
            "error": "unknown_command",
            "message": "Неизвестная команда. Используйте /help для списка команд."
        })


from chats.models import ChatSession, ChatMessage
from subscriptions.services.usage_limits import consume_user_token


def handle_ai_question_from_telegram(tg_profile, question):
    try:
        session = get_or_create_telegram_session(tg_profile)

        user = tg_profile.user

        if user:
            limit_response = consume_user_token(user)

            if limit_response:
                return {
                    "ok": False,
                    "error": "limit_exceeded",
                    "message": "У вас закончились бесплатные запросы."
                }

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        payload = {
            "question": question,
            "session_id": session.id
        }

        r = requests.post(
            "https://etha-hypercatalectic-rueben.ngrok-free.dev/ask",
            json=payload,
            timeout=120,
        )

        r.raise_for_status()

        data = r.json()

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=json.dumps(data, ensure_ascii=False)
        )

        return data

    except Exception:
        traceback.print_exc()

        return {
            "ok": False,
            "error": "ai_request_failed",
            "message": "Ошибка при обращении к ИИ."
        }


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
            return {
                "ok": False,
                "error": "limit_exceeded",
                "message": "У вас закончились бесплатные запросы."
            }

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        r = requests.post(
            "https://etha-hypercatalectic-rueben.ngrok-free.dev/price",
            json={
                "question": question,
                "session_id": session.id
            },
            timeout=120,
        )

        r.raise_for_status()

        data = r.json()

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=json.dumps(data, ensure_ascii=False)
        )

        return data

    except Exception:
        traceback.print_exc()

        return {
            "ok": False,
            "error": "price_request_failed",
            "message": "Ошибка при расчёте стоимости дела."
        }

def handle_win_chance_question(tg_profile, question):
    try:
        session = get_or_create_telegram_session(tg_profile)
        user = tg_profile.user

        limit_response = consume_user_token(user)

        if limit_response:
            return {
                "ok": False,
                "error": "limit_exceeded",
                "message": "У вас закончились бесплатные запросы."
            }

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        r = requests.post(
            "https://etha-hypercatalectic-rueben.ngrok-free.dev/article-win-chance",
            json={
                "question": question,
                "session_id": session.id
            },
            timeout=120,
        )

        r.raise_for_status()

        data = r.json()

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=json.dumps(data, ensure_ascii=False)
        )

        return data

    except Exception:
        traceback.print_exc()

        return {
            "ok": False,
            "error": "win_chance_request_failed",
            "message": "Ошибка при анализе шансов."
        }


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
        return {
            "ok": False,
            "error": "document_not_found",
            "message": "Документ не найден. Напишите /docs, чтобы посмотреть список документов."
        }

    document = get_document(found_template)

    tg_profile.current_template_name = found_template
    tg_profile.save(update_fields=["current_template_name", "updated_at"])

    response_data = {
        "ok": True,
        "type": "document_selected",
        "template_name": found_template,
        "title": document["title"],
        "fields": document["fields"],
        "message": "Документ выбран. Заполните поля и отправьте /generate JSON."
    }

    ChatMessage.objects.create(
        session=session,
        role="assistant",
        content=json.dumps(response_data, ensure_ascii=False)
    )

    return response_data


def handle_telegram_document_generate(tg_profile, raw_json):
    try:
        session = get_or_create_telegram_session(tg_profile)
        user = tg_profile.user

        template_name = tg_profile.current_template_name

        if not template_name:
            return {
                "ok": False,
                "error": "template_not_selected",
                "message": "Сначала выберите документ через /doc название документа."
            }

        if template_name not in DOCUMENT_TYPES:
            return {
                "ok": False,
                "error": "template_not_found",
                "message": "Выбранный документ больше не найден. Выберите заново через /docs."
            }

        try:
            values = json.loads(raw_json)
        except json.JSONDecodeError:
            return {
                "ok": False,
                "error": "invalid_json",
                "message": 'Ошибка JSON. Отправьте данные в формате: /generate {"field": "value"}'
            }

        if not isinstance(values, dict):
            return {
                "ok": False,
                "error": "invalid_json_type",
                "message": "После /generate должен быть JSON-объект."
            }

        document = get_document(template_name)

        required_keys = [
            field["key"] for field in document["fields"] if field.get("required")
        ]

        missing = [key for key in required_keys if not values.get(key)]

        if missing:
            return {
                "ok": False,
                "error": "missing_required_fields",
                "missing_fields": missing,
                "message": "Заполнены не все обязательные поля."
            }

        limit_response = consume_user_token(user)

        if limit_response:
            return {
                "ok": False,
                "error": "limit_exceeded",
                "message": "У вас закончились бесплатные запросы."
            }

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=f"Создание документа: {template_name}"
        )

        generator_response = send_to_generator(
            template_name=template_name,
            values=values
        )

        if generator_response.get("error"):
            return {
                "ok": False,
                "error": "document_generation_failed",
                "message": "Ошибка при создании документа.",
                "details": generator_response
            }

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=json.dumps(generator_response, ensure_ascii=False)
        )

        return generator_response

    except Exception:
        traceback.print_exc()

        return {
            "ok": False,
            "error": "document_generation_exception",
            "message": "Ошибка при создании документа."
        }

def handle_top_lawyers_question(tg_profile, question):
    try:
        session = get_or_create_telegram_session(tg_profile)
        user = tg_profile.user

        limit_response = consume_user_token(user)

        if limit_response:
            return {
                "ok": False,
                "error": "limit_exceeded",
                "message": "У вас закончились бесплатные запросы."
            }

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

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=json.dumps(data, ensure_ascii=False)
        )

        return data

    except Exception:
        traceback.print_exc()

        return {
            "ok": False,
            "error": "top_lawyers_request_failed",
            "message": "Ошибка при поиске топ адвокатов."
        }
    
def get_telegram_subscription_plans():
    plans = get_subscription_plans_for_response()

    return {
        "ok": True,
        "type": "subscription_plans",
        "plans": plans,
        "message": (
            "Доступные тарифы:\n"
            "1 месяц — /subscribe 1m\n"
            "6 месяцев — /subscribe 6m\n"
            "1 год — /subscribe 1y"
        )
    }


def create_telegram_subscription_invoice(tg_profile, plan):
    user = tg_profile.user

    if not user:
        return {
            "ok": False,
            "error": "not_authenticated",
            "message": "Сначала выполните вход через /login или регистрацию через /register."
        }

    if plan not in SUBSCRIPTION_PLANS:
        return {
            "ok": False,
            "error": "invalid_plan",
            "message": "Неверный тариф. Используйте: /subscribe 1m, /subscribe 6m или /subscribe 1y"
        }

    payment = create_subscription_payment(
        user=user,
        plan=plan
    )

    payment_url = build_robokassa_url(
        payment=payment,
        email=user.email
    )

    plan_data = SUBSCRIPTION_PLANS[plan]

    return {
        "ok": True,
        "type": "telegram_subscription_invoice_created",
        "invoice_id": payment.invoice_id,
        "plan": plan,
        "amount": str(plan_data["amount"]),
        "payment_url": payment_url,
        "message": (
            f"Счёт на оплату создан.\n"
            f"Тариф: {plan_data['title']}\n"
            f"Сумма: {plan_data['amount']} ₸\n\n"
            f"Ссылка для оплаты:\n{payment_url}\n\n"
            f"После оплаты отправьте команду /subscription, чтобы проверить статус подписки."
        )
    }


def get_telegram_subscription_status(tg_profile):
    user = tg_profile.user

    if not user:
        return {
            "ok": False,
            "error": "not_authenticated",
            "message": "Сначала выполните вход через /login или регистрацию через /register."
        }

    now_time = timezone.now()

    subscription = (
        Subscription.objects
        .filter(
            user=user,
            end_date__gt=now_time
        )
        .order_by("-end_date")
        .first()
    )

    if not subscription:
        return {
            "ok": True,
            "type": "subscription_status",
            "active": False,
            "message": "Активной подписки нет. Для выбора тарифа отправьте /plans."
        }

    return {
        "ok": True,
        "type": "subscription_status",
        "active": True,
        "plan": subscription.plan,
        "start_date": subscription.start_date.isoformat(),
        "end_date": subscription.end_date.isoformat(),
        "message": f"Подписка активна до {subscription.end_date.strftime('%d.%m.%Y %H:%M')}."
    }