from django.contrib import admin
from django.urls import path
from users.views import *

app_name = "users"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrations/', Registrations.as_view(), name='Registrations'),
    path('login/', LoginView.as_view(), name='LoginView'),
    path('logout/', LogoutView.as_view(), name='LogoutView'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
]
