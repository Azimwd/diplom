from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import now
import requests

from .models import ChatSession, ChatMessage
from .serializers import ChatMessageSerializer, ChatSessionListSerializer
from chats.pagination import ChatPagination
from subscriptions.models import Subscription

from django.http import StreamingHttpResponse
from users.authentication import CookieAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes

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

        active_sub = (
            Subscription.objects
            .filter(user=user, end_date__gt=now())
            .order_by("-end_date")
            .first()
        )

        if not active_sub:
            if user.freeRequest <= 0:
                return Response(
                    {"message": "Нет доступных запросов"},
                    status=402
                )
            user.freeRequest -= 1
            user.save()

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

@api_view(["GET"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def stream_chat_answer(request, session_id):
    user = request.user

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
                json={"question": last_user_message.content},
                timeout=60
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

    return StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream; charset=utf-8"
    )
