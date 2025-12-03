from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer

class ChatSessionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        title = request.data.get("title", "")
        session = ChatSession.objects.create(user=request.user, title=title)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ChatSessionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, session_id, user):
        try:
            return ChatSession.objects.get(id=session_id, user=user)
        except ChatSession.DoesNotExist:
            return None

    def get(self, request, session_id):
        session = self.get_object(session_id, request.user)
        if not session:
            return Response({"detail": "Сессия не найдена."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)

    def patch(self, request, session_id):
 
        session = self.get_object(session_id, request.user)
        if not session:
            return Response({"detail": "Сессия не найдена."}, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get("title")
        if title is None:
            return Response({"detail": "Не указано новое название."}, status=status.HTTP_400_BAD_REQUEST)

        session.title = title
        session.save()
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, session_id):
        session = self.get_object(session_id, request.user)
        if not session:
            return Response({"detail": "Сессия не найдена."}, status=status.HTTP_404_NOT_FOUND)

        session.delete()
        return Response({"detail": "Сессия успешно удалена."}, status=status.HTTP_204_NO_CONTENT)



class ChatMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({"detail": "Сессия не найдена."}, status=status.HTTP_404_NOT_FOUND)

        content = request.data.get("content")
        if not content:
            return Response({"detail": "Сообщение не может быть пустым."}, status=status.HTTP_400_BAD_REQUEST)

        ChatMessage.objects.create(session=session, role="user", content=content)

        assistant_content = f"Ответ на: {content}"
        ChatMessage.objects.create(session=session, role="assistant", content=assistant_content)

        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
