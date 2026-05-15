from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
import requests

from .models import ChatSession, ChatMessage
from .serializers import ChatMessageSerializer, ChatSessionListSerializer
from chats.pagination import ChatPagination
from subscriptions.services.usage_limits import consume_user_token

from django.http import StreamingHttpResponse
from users.authentication import CookieAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status


# Список сессий с пагинацией
class ChatSessionListView(ListAPIView):
    pagination_class = ChatPagination
    serializer_class = ChatSessionListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(
            user=self.request.user
        ).order_by("-updated_at")


# Создание сессии
class ChatSessionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get("title", "")
        session = ChatSession.objects.create(user=request.user, title=title)
        serializer = ChatSessionListSerializer(session)

        return Response({
            **serializer.data,    
            "message": "Сессия успешно создана" 
        }, status=201)


# Детали сессии и управление
class ChatSessionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ChatPagination

    def get_object(self, session_id, user):
        return ChatSession.objects.filter(id=session_id, user=user).first()

    def get(self, request, session_id):
        session = self.get_object(session_id, request.user)
        if not session:
            return Response({"message": "Сессия не найдена"}, status=404)

        messages = session.messages.order_by('-created_at')
        paginator = self.pagination_class()
        paginated_messages = paginator.paginate_queryset(messages, request)
        serializer = ChatMessageSerializer(paginated_messages, many=True)

        data = {
            'id': session.id,
            'title': session.title,
            'messages': serializer.data,
            'created_at': session.created_at,
            'updated_at': session.updated_at,
        }

        return paginator.get_paginated_response({
            "data": data,
            "message": "Сессия успешно загружена"
        })

    def patch(self, request, session_id):
        session = self.get_object(session_id, request.user)
        if not session:
            return Response({"message": "Сессия не найдена"}, status=404)

        new_title = request.data.get("title")
        if not new_title:
            return Response({"message": "Не передан новый заголовок"}, status=400)

        session.title = new_title
        session.save()
        serializer = ChatSessionListSerializer(session)

        return Response({
            **serializer.data,
            "message": "Название сессии обновлено"
        }, status=200)

    def delete(self, request, session_id):
        session = self.get_object(session_id, request.user)
        if not session:
            return Response({"message": "Сессия не найдена"}, status=404)

        session.delete()
        return Response({"message": "Сессия удалена"}, status=204)


class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        user = request.user

        limit_response = consume_user_token(user)
        if limit_response:
            return limit_response

        session = ChatSession.objects.filter(
            id=session_id,
            user=user
        ).first()

        if not session:
            return Response(
                {"message": "Сессия не найдена"},
                status=404
            )

        content = request.data.get("content")

        if not content:
            return Response(
                {"message": "Не передан контент сообщения"},
                status=400
            )

        message = ChatMessage.objects.create(
            session=session,
            role="user",
            content=content
        )

        return Response({
            "message": "Сообщение сохранено",
            "message_id": message.id
        }, status=201)

def stream_chat_answer(request, session_id):
    auth = CookieAuthentication()

    try:
        user_auth_tuple = auth.authenticate(request)
        if user_auth_tuple is None:
            return StreamingHttpResponse(
                "data: Не авторизован\n\n",
                content_type="text/event-stream; charset=utf-8",
                status=401
            )
        user, _ = user_auth_tuple
        request.user = user
    except AuthenticationFailed:
        return StreamingHttpResponse(
            "data: Не авторизован\n\n",
            content_type="text/event-stream; charset=utf-8",
            status=401
        )

    session = ChatSession.objects.filter(
        id=session_id,
        user_id=user.id
    ).first()

    if not session:
        return StreamingHttpResponse(
            "data: Сессия не найдена\n\n",
            content_type="text/event-stream; charset=utf-8",
            status=404
        )

    last_user_message = (
        ChatMessage.objects
        .filter(session=session, role="user")
        .order_by("-created_at")
        .first()
    )

    if not last_user_message:
        return StreamingHttpResponse(
            "data: Нет сообщения пользователя\n\n",
            content_type="text/event-stream; charset=utf-8"
        )

    def event_stream():
        try:
            r = requests.post(
                "https://etha-hypercatalectic-rueben.ngrok-free.dev/ask",
                json={"question": last_user_message.content, "session_id": session.id},
                timeout=120
            )
            r.raise_for_status()

            api_result = r.json()
            answer = api_result.get("answer", "Нет ответа от API.")

            for char in answer:
                yield f"data: {char}\n\n"

            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=answer
            )

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: Ошибка: {str(e)}\n\n"

    response = StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream; charset=utf-8"
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"

    return response

# ______________
# Calculator AI
# ______________

class AttorneyPriceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        user = request.user

        session = ChatSession.objects.filter(
            id=session_id,
            user=user
        ).first()

        if not session:
            return Response(
                {"message": "Сессия не найдена"},
                status=404
            )

        question = request.data.get("question", "").strip()

        if not question:
            return Response(
                {"error": "question обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        limit_response = consume_user_token(user)
        if limit_response:
            return limit_response

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        try:
            r = requests.post(
                "https://etha-hypercatalectic-rueben.ngrok-free.dev/price",
                json={
                    "question": question,
                    "session_id": session.id
                },
                timeout=120
            )

            r.raise_for_status()
            ai_result = r.json()

            answer = ai_result.get("answer", "Нет ответа от ИИ")

            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=answer
            )

            return Response({
                "answer": answer,
                "intent": ai_result.get("intent"),
                "session_id": session.id,
            })

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Ошибка при запросе к ИИ: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY
            )
        
class ArticleWinChanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        user = request.user

        session = ChatSession.objects.filter(
            id=session_id,
            user=user
        ).first()

        if not session:
            return Response(
                {"message": "Сессия не найдена"},
                status=404
            )

        question = request.data.get("question", "").strip()

        if not question:
            return Response(
                {"error": "question обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        limit_response = consume_user_token(user)
        if limit_response:
            return limit_response

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        try:
            r = requests.post(
                "https://etha-hypercatalectic-rueben.ngrok-free.dev/article-win-chance",
                json={
                    "question": question,
                    "session_id": session.id
                },
                timeout=120
            )

            r.raise_for_status()
            ai_result = r.json()

            answer = ai_result.get("answer", "Нет ответа от ИИ")

            content_data = {
                "type": "article_win_chance",
                "intent": ai_result.get("intent"),
                "found": ai_result.get("found"),
                "answer": answer,

                "article": ai_result.get("article"),
                "requested_article": ai_result.get("requested_article"),

                "total": ai_result.get("total"),
                "wins": ai_result.get("wins"),
                "losses": ai_result.get("losses"),
                "partial_wins": ai_result.get("partial_wins"),
                "remanded": ai_result.get("remanded"),
                "dismissed": ai_result.get("dismissed"),
                "unknown": ai_result.get("unknown"),

                "win_rate": ai_result.get("win_rate"),
                "loss_rate": ai_result.get("loss_rate"),
                "lawyer_case_links": ai_result.get("lawyer_case_links"),

                "detector_source": ai_result.get("detector_source"),
                "confidence": ai_result.get("confidence"),

                "session_id": session.id,
            }

            content_json = json.dumps(content_data, ensure_ascii=False)

            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=content_json
            )

            return Response({
                "content": content_json
            })


        except requests.exceptions.Timeout:
            return Response(
                {"error": "ИИ-сервис долго не отвечает"},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Ошибка при запросе к ИИ: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY
            )
        

class TopLawyersByArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        user = request.user

        session = ChatSession.objects.filter(
            id=session_id,
            user=user
        ).first()

        if not session:
            return Response(
                {"message": "Сессия не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        question = request.data.get("question", "").strip()
        top_n = request.data.get("top_n", 5)

        if not question:
            return Response(
                {"error": "question обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        limit_response = consume_user_token(user)
        if limit_response:
            return limit_response

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=question
        )

        try:
            r = requests.post(
                "https://etha-hypercatalectic-rueben.ngrok-free.dev/top-lawyers-by-article",
                json={
                    "question": question,
                    "top_n": top_n,
                    "session_id": session.id
                },
                timeout=120
            )

            r.raise_for_status()
            ai_result = r.json()

            answer = ai_result.get("answer", "Нет ответа от ИИ")

            content_data = {
                "type": "top_lawyers_by_article",
                "intent": ai_result.get("intent"),
                "found": ai_result.get("found"),
                "answer": answer,

                "article": ai_result.get("article"),
                "requested_article": ai_result.get("requested_article"),
                "total_lawyers": ai_result.get("total_lawyers"),
                "lawyers": ai_result.get("lawyers", []),

                "detector_source": ai_result.get("detector_source"),
                "confidence": ai_result.get("confidence"),

                "session_id": session.id,
            }

            content_json = json.dumps(content_data, ensure_ascii=False)

            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=content_json
            )

            return Response(
                {
                    "content": content_json
                },
                status=status.HTTP_200_OK
            )

        except requests.exceptions.Timeout:
            return Response(
                {"error": "ИИ-сервис долго не отвечает"},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Ошибка при запросе к ИИ: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY
            )