from django.contrib import admin
from django.urls import path
from users.views import *

app_name = "users"
urlpatterns = [
    path('registrations/', Registrations.as_view(), name='Registrations'),
    path('login/', LoginView.as_view(), name='LoginView'),
    path('logout/', LogoutView.as_view(), name='LogoutView'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),

    path("google/login/", google_login_view, name="google-login"),
    path("google/callback/", google_callback_view, name="google-callback"),
]
