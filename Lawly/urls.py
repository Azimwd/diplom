from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from users.urls import google_callback_view
urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("profile/", include("user_profile.urls")),
    path("settings/", include("settings.urls")),
    path("chats/", include("chats.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("payments/", include("payments.urls")),
    path('accounts/google/login/callback/', google_callback_view, name='google_token_callback'),
    path("ai-documents/", include("ai_documents.urls")),
    path("telegram_bot/", include("telegram_bot.urls")),
    path("ai_modules/", include("ai_modules.urls")),
]

urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]