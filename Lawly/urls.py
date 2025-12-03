from argparse import Namespace
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace="users")),
    path('profile/', include('user_profile.urls', namespace="profile")),
    path('settings/', include('settings.urls', namespace="settings")),
    path('chats/', include('chats.urls', namespace="chats")),
    path('subscriptions/', include('subscriptions.urls', namespace="subscriptions")),
    path('payments/', include('payments.urls', namespace="payments")),
]