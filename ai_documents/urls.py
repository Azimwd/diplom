from django.urls import path
from .views import AiDocumentChatView, DocumentsListView

app_name = "ai_documents"

urlpatterns = [
    path(
        "sessions/<int:session_id>/documents/",
        AiDocumentChatView.as_view()
    ),
]