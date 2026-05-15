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