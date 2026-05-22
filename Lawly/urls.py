from argparse import Namespace
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('profile/', include('user_profile.urls')),
    path('settings/', include('settings.urls')),
    path('chats/', include('chats.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('payments/', include('payments.urls')),
    path('accounts/', include('allauth.urls')),
    path('ai-documents/', include('ai_documents.urls')),
    path('telegram_bot/', include('telegram_bot.urls')),
    path('ai_modules/', include('ai_modules.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)