import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from chats.models import ChatSession, ChatMessage

from .services.documents import DOCUMENT_TYPES, get_document, get_documents_list
from .services.ai_detector import detect_document_type
from .services.generator_client import send_to_generator


class AiDocumentChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get_session(self, session_id, user):
        return ChatSession.objects.filter(
            id=session_id,
            user=user
        ).first()

    def post(self, request, session_id):
        session = self.get_session(session_id, request.user)

        if not session:
            return Response(
                {"detail": "Сессия не найдена."},
                status=status.HTTP_404_NOT_FOUND
            )

        action = request.data.get("action")
        question = request.data.get("question", "").strip()
        template_name = request.data.get("template_name")
        values = request.data.get("values")

        if action == "ask":
            return self.handle_ask(session, question)

        if action == "select":
            return self.handle_select(session, template_name)

        if action == "generate":
            return self.handle_generate(session, template_name, values)

        return Response(
            {
                "detail": "Передайте action: ask, select или generate."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def save_message(self, session, role, content):
        if not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=False)

        return ChatMessage.objects.create(
            session=session,
            role=role,
            content=content
        )

    # 1. Пользователь пишет: "какие документы можно создать?"
    # или "создай мне договор"
    def handle_ask(self, session, question):
        if not question:
            return Response(
                {"detail": "Поле question обязательно."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.save_message(session, "user", question)

        detected = detect_document_type(question)

        # Если ИИ понял, что пользователь просит список документов
        if detected.get("intent") == "documents_list":
            payload = {
                "type": "documents_list",
                "reply": "Вы можете создать следующие документы:",
                "documents": get_documents_list(),
                "next_step": "select_document"
            }

            self.save_message(session, "assistant", payload)

            return Response(payload)

        # Если ИИ определил конкретный документ
        if detected.get("found"):
            template_name = detected.get("template_name")

            if template_name not in DOCUMENT_TYPES:
                payload = {
                    "type": "documents_list",
                    "reply": "ИИ вернул неизвестный документ. Выберите документ из списка.",
                    "documents": get_documents_list(),
                    "next_step": "select_document"
                }

                self.save_message(session, "assistant", payload)

                return Response(payload)

            document = get_document(template_name)

            payload = {
                "type": "document_fields",
                "reply": f"Составить {document['title'].lower()}?",
                "template_name": template_name,
                "document_title": document["title"],
                "fields": document["fields"],
                "next_step": "generate_document"
            }

            self.save_message(session, "assistant", payload)

            return Response(payload)

        # Если ИИ не понял документ
        payload = {
            "type": "documents_list",
            "reply": "Я не смог точно определить документ. Выберите документ из списка.",
            "documents": get_documents_list(),
            "next_step": "select_document"
        }

        self.save_message(session, "assistant", payload)

        return Response(payload)

    # 2. Пользователь выбрал документ из списка
    def handle_select(self, session, template_name):
        if not template_name:
            return Response(
                {"detail": "Поле template_name обязательно."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if template_name not in DOCUMENT_TYPES:
            return Response(
                {"detail": "Такой документ не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        document = get_document(template_name)

        user_payload = {
            "type": "document_selected",
            "template_name": template_name,
            "document_title": document["title"]
        }

        self.save_message(session, "user", user_payload)

        assistant_payload = {
            "type": "document_fields",
            "reply": f"Заполните поля для документа: {document['title']}",
            "template_name": template_name,
            "document_title": document["title"],
            "fields": document["fields"],
            "next_step": "generate_document"
        }

        self.save_message(session, "assistant", assistant_payload)

        return Response(assistant_payload)

    # 3. Пользователь отправляет template_name + values
    # Django отправляет это в /generate и сохраняет ссылку в историю чата
    def handle_generate(self, session, template_name, values):
        if not template_name:
            return Response(
                {"detail": "Поле template_name обязательно."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not values or not isinstance(values, dict):
            return Response(
                {"detail": "Поле values обязательно и должно быть объектом."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if template_name not in DOCUMENT_TYPES:
            return Response(
                {"detail": "Такой документ не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        document = get_document(template_name)

        required_keys = [
            field["key"]
            for field in document["fields"]
            if field.get("required")
        ]

        missing = [
            key for key in required_keys
            if not values.get(key)
        ]

        if missing:
            return Response(
                {
                    "detail": "Заполнены не все обязательные поля.",
                    "missing_fields": missing,
                    "fields": document["fields"]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_payload = {
            "type": "document_values",
            "template_name": template_name,
            "document_title": document["title"],
            "values": values
        }

        self.save_message(session, "user", user_payload)

        generator_response = send_to_generator(
            template_name=template_name,
            values=values
        )

        if generator_response.get("error"):
            return Response(
                {
                    "detail": "Ошибка внешнего генератора.",
                    "generator_response": generator_response
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        response_data = generator_response.get("response", {})

        file_url = (
            response_data.get("file_url")
            or response_data.get("download_url")
            or response_data.get("url")
        )

        assistant_payload = {
            "type": "document_generated",
            "reply": "Документ успешно сгенерирован.",
            "template_name": template_name,
            "document_title": document["title"],
            "file_url": file_url,
            "generator_response": generator_response
        }

        self.save_message(session, "assistant", assistant_payload)

        return Response(assistant_payload)