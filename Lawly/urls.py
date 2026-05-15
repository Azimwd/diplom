from argparse import Namespace
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace="users")),
    path('profile/', include('user_profile.urls', namespace="profile")),
    path('settings/', include('settings.urls', namespace="settings")),
    path('chats/', include('chats.urls', namespace="chats")),
    path('subscriptions/', include('subscriptions.urls', namespace="subscriptions")),
    path('payments/', include('payments.urls', namespace="payments")),
    path('accounts/', include('allauth.urls')),
    path('telegram-bot/', include('telegram_bot.urls')),
    path('ai-documents/', include('ai_documents.urls')),
    path('telegram_bot/', include('telegram_bot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)