from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from chats.models import ChatSession, ChatMessage
from subscriptions.services.usage_limits import consume_user_token
import requests
import json

# ______________
# Ask AI
# ______________
class AskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        user = request.user

        session = ChatSession.objects.filter(
            id=session_id,
            user=user
        ).first()

        if not session:
            return Response(
                {"error": "Сессия не найдена"},
                status=404
            )

        question = request.data.get("question", "").strip()

        if not question:
            return Response(
                {"error": "question обязателен"},
                status=400
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
                "https://etha-hypercatalectic-rueben.ngrok-free.dev/ask",
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
                "session_id": session.id
            })

        except requests.exceptions.Timeout:
            return Response(
                {"error": "ИИ долго отвечает"},
                status=504
            )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)},
                status=502
            )

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