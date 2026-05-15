from django.contrib import admin
from django.urls import path
from chats.views import *

app_name = "chats"

urlpatterns = [
    path("sessions/", ChatSessionListView.as_view(), name="chat-session-list"),
    path("sessions/create/", ChatSessionCreateView.as_view(), name="chat-session-create"),
    path('sessions/<int:session_id>/', ChatSessionDetailView.as_view(), name='chat-session-detail'),
    path('sessions/<int:session_id>/messages/', ChatMessageView.as_view(), name='chat-messages'),
]