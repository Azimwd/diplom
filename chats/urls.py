from django.contrib import admin
from django.urls import path
from chats.views import *

app_name = "chats"

urlpatterns = [
    path("sessions/", ChatSessionListView.as_view(), name="chat-session-list"),
    path("sessions/create/", ChatSessionCreateView.as_view(), name="chat-session-create"),
    path('sessions/<int:session_id>/', ChatSessionDetailView.as_view(), name='chat-session-detail'),
    
    path('sessions/<int:session_id>/messages/', ChatMessageView.as_view(), name='chat-messages'),
    path("sessions/<int:session_id>/stream/", stream_chat_answer),
    
    path("sessions/<int:session_id>/attorney-price/", AttorneyPriceView.as_view()),

    path("sessions/<int:session_id>/article-win-chance/", ArticleWinChanceView.as_view()),
    
    path("sessions/<int:session_id>/top-lawyers/", TopLawyersByArticleView.as_view(),name="top-lawyers-by-article"),
]