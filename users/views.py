from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import generics, status, serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from user_profile.models import Profile
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
import requests
from django.http import HttpResponse
from rest_framework.exceptions import ErrorDetail
from django.utils import timezone
from .models import SocialOnboardingSession, Users

ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"
SESSION_FLAG_COOKIE = "has_session"

ACCESS_MAX_AGE = 60 * 60
REFRESH_MAX_AGE = 30 * 24 * 60 * 60

COOKIE_SECURE = True
COOKIE_HTTPONLY = True
COOKIE_SAMESITE = "None"
COOKIE_DOMAIN = None

User = get_user_model()

def resend_verification_email(email: str, link: str) -> None:
    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": "Lawly <noreply@yurgid.kz>",
            "to": [email],
            "subject": "Подтверждение регистрации на Lawly",
            "html": f"""
                <div style="font-family: Arial, sans-serif; line-height: 1.5;">
                    <h2>Подтверждение регистрации</h2>
                    <p>Чтобы продолжить регистрацию, подтвердите email:</p>
                    <p>
                        <a href="{link}" style="display:inline-block;padding:10px 16px;
                        text-decoration:none;border-radius:6px;border:1px solid #ccc;">
                            Подтвердить email
                        </a>
                    </p>
                    <p>Если кнопка не работает, откройте ссылку вручную:</p>
                    <p>{link}</p>
                </div>
            """,
        },
        timeout=15,
    )
    response.raise_for_status()

def send_password_reset_email(email: str, link: str) -> None:
    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": "YurGid <noreply@yurgid.kz>",
            "to": [email],
            "subject": "Сброс пароля на Lawly",
            "html": f"""
                <div style="font-family: Arial, sans-serif; line-height: 1.5;">
                    <h2>Сброс пароля</h2>
                    <p>Чтобы установить новый пароль, перейдите по ссылке:</p>
                    <p>
                        <a href="{link}" style="display:inline-block;padding:10px 16px;
                        text-decoration:none;border-radius:6px;border:1px solid #ccc;">
                            Сбросить пароль
                        </a>
                    </p>
                    <p>Если кнопка не работает, откройте ссылку вручную:</p>
                    <p>{link}</p>
                </div>
            """,
        },
        timeout=15,
    )
    response.raise_for_status()

@ensure_csrf_cookie
def csrf_token_view(request):
    csrf_token = get_token(request)
    response = JsonResponse({"csrf_token": csrf_token})
    response.set_cookie(
        key="csrftoken",
        value=csrf_token,
        httponly=False,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        path="/",
        domain=COOKIE_DOMAIN,
    )
    return response


class ValidateTokenView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response(
            {
                "valid": True,
                "user_id": user.id,
                "email": user.email,
            }
        )


class SocialCompleteSerializer(serializers.Serializer):
    social_session = serializers.UUIDField()
    role = serializers.ChoiceField(Users.ROLE_CHOICES)

    def validate(self, data):
        try:
            s = SocialOnboardingSession.objects.select_related("user").get(
                session_id=data["social_session"]
            )
        except SocialOnboardingSession.DoesNotExist:
            raise serializers.ValidationError("Сессия не найдена")

        if s.expires_at <= timezone.now():
            raise serializers.ValidationError("Сессия истекла")

        self.session_obj = s
        return data

    def save(self):
        user = self.session_obj.user
        user.role = self.validated_data["role"]
        user.save(update_fields=["role"])
        self.session_obj.delete()
        return user

class SocialCompleteView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = SocialCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        response = Response({"success": True}, status=200)

        response.set_cookie(
            key=ACCESS_COOKIE_NAME,
            value=str(refresh.access_token),
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=ACCESS_MAX_AGE,
            path="/",
            domain=COOKIE_DOMAIN,
        )

        response.set_cookie(
            key=REFRESH_COOKIE_NAME,
            value=str(refresh),
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=REFRESH_MAX_AGE,
            path="/",
            domain=COOKIE_DOMAIN,
        )

        response.set_cookie(
            key=SESSION_FLAG_COOKIE,
            value="1",
            httponly=False,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            path="/",
            domain=COOKIE_DOMAIN,
        )

        csrf_token = get_token(request)
        response.set_cookie(
            key="csrftoken",
            value=csrf_token,
            httponly=False,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            path="/",
            domain=COOKIE_DOMAIN,
        )

        return response

import urllib.parse
def google_login_view(request):
    redirect_uri = "https://lawly.up.railway.app/users/google/callback/"

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account",
    }

    google_url = "https://accounts.google.com/o/oauth2/v2/auth"

    return redirect(f"{google_url}?{urllib.parse.urlencode(params)}")

class Registrations(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                 "user_id": user.id,
                "message": "Регистрация завершена"
            }, status=status.HTTP_201_CREATED)
        
        errors = serializer.errors

        def get_first_error(errs):
            if isinstance(errs, list) and errs:
                return str(errs[0])
            elif isinstance(errs, dict) and errs:
                return get_first_error(next(iter(errs.values())))
            return None

        first_error = get_first_error(errors)

        return Response({
            "message": first_error or "Ошибка валидации"
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        

        csrf_token = get_token(request)

        response = Response(
            {
                "id": user.id,
                "email": user.email,
                "role": getattr(user, "role", None),
                "csrf_token": csrf_token,
                "message": "Успешный вход",
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key=ACCESS_COOKIE_NAME,
            value=access_token,
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=ACCESS_MAX_AGE,
            path="/",
            domain=COOKIE_DOMAIN,
        )
        response.set_cookie(
            key=REFRESH_COOKIE_NAME,
            value=refresh_token,
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=REFRESH_MAX_AGE,
            path="/",
            domain=COOKIE_DOMAIN,
        )
        response.set_cookie(
            key=SESSION_FLAG_COOKIE,
            value="1",
            httponly=False,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            path="/",
            domain=COOKIE_DOMAIN,
        )
        csrf_token = get_token(request)
        response.set_cookie(
            key="csrftoken",
            value=csrf_token,
            httponly=False,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            path="/",
            domain=COOKIE_DOMAIN,
        )

        return response


class SessionPingView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        refresh = request.COOKIES.get(REFRESH_COOKIE_NAME)
        if not refresh:
            return Response(
                {"detail": "No session"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            RefreshToken(refresh)
            return Response({"ok": True}, status=status.HTTP_200_OK)
        except TokenError:
            resp = Response(
                {"detail": "Session expired"}, status=status.HTTP_401_UNAUTHORIZED
            )
            clear_auth_cookies(resp)
            return resp


def clear_auth_cookies(response):
    response.delete_cookie(
        key=ACCESS_COOKIE_NAME,
        path="/",
        samesite="None",
    )

    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path="/",
        samesite="None",
    )

    response.delete_cookie(
        key=SESSION_FLAG_COOKIE,
        path="/",
        samesite="None",
    )

    response.delete_cookie(
        key="csrftoken",
        path="/",
        samesite="None",
    )

    return response

class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                pass

        response = Response(
            {
                "statusCode": 200,
                "success": True,
                "data": None,
                "message": "Успешный выход",
            },
            status=status.HTTP_200_OK,
        )

        clear_auth_cookies(response)

        return response


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        old_refresh = request.COOKIES.get(REFRESH_COOKIE_NAME)
        if not old_refresh:
            return Response(
                {"detail": "No refresh"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(old_refresh)
        except TokenError:
            resp = Response(
                {"detail": "Invalid refresh"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            clear_auth_cookies(resp)
            return resp

        user_id = refresh.get("user_id")
        if not user_id:
            resp = Response(
                {"detail": "Invalid refresh payload"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            clear_auth_cookies(resp)
            return resp

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            resp = Response(
                {"detail": "User not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            clear_auth_cookies(resp)
            return resp

        new_refresh = RefreshToken.for_user(user)
        new_access = str(new_refresh.access_token)

        csrf_token = get_token(request)

        resp = Response(
            {
                "success": True,
                "csrf_token": csrf_token,
            },
            status=status.HTTP_200_OK,
        )

        resp.set_cookie(
            key=ACCESS_COOKIE_NAME,
            value=new_access,
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=ACCESS_MAX_AGE,
            path="/",
            domain=COOKIE_DOMAIN,
        )

        resp.set_cookie(
            key=REFRESH_COOKIE_NAME,
            value=str(new_refresh),
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=REFRESH_MAX_AGE,
            path="/",
            domain=COOKIE_DOMAIN,
        )

        resp.set_cookie(
            key=SESSION_FLAG_COOKIE,
            value="1",
            httponly=False,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            path="/",
            domain=COOKIE_DOMAIN,
        )

        csrf_token = get_token(request)
        resp.set_cookie(
            key="csrftoken",
            value=csrf_token,
            httponly=False,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            path="/",
            domain=COOKIE_DOMAIN,
        )

        return resp


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        response = Response(
            {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "message": "Успешный вход",
            },
            status=status.HTTP_200_OK,
        )

        return response


def first_error_message(detail) -> str:
    if isinstance(detail, dict):
        for v in detail.values():
            return first_error_message(v)
        return "Ошибка валидации"

    if isinstance(detail, list):
        return first_error_message(detail[0]) if detail else "Ошибка валидации"

    if isinstance(detail, ErrorDetail):
        return str(detail)

    return str(detail)


class RequestPasswordResetEmail(generics.GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email", "").strip().lower()

        print("RESET EMAIL REQUEST:", email)

        if not email:
            return Response(
                {
                    "statusCode": 400,
                    "success": False,
                    "message": "Email не передан",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email__iexact=email).first()

        if not user:
            print("USER NOT FOUND:", email)

            # Только для теста. В продакшене лучше не раскрывать, есть ли email в базе.
            return Response(
                {
                    "statusCode": 404,
                    "success": False,
                    "message": "Пользователь с таким email не найден",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = (
            f"{settings.FRONTEND_URL}/login/forgot-password/"
            f"?uidb64={uidb64}&token={token}"
        )
        print("RESET URL:", reset_link)

        try:
            result = send_password_reset_email(user.email, reset_link)
            print("RESEND RESULT:", result)
        except Exception as e:
            print("EMAIL SEND ERROR:", str(e))

            return Response(
                {
                    "statusCode": 500,
                    "success": False,
                    "message": f"Ошибка отправки письма: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "statusCode": 200,
                "success": True,
                "message": "На вашу почту была отправлена ссылка для восстановления пароля",
            },
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {
                        "statusCode": 400,
                        "success": False,
                        "data": None,
                        "message": "Ссылка недействительна",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {
                    "statusCode": 200,
                    "success": True,
                    "data": {"uidb64": uidb64, "token": token},
                    "message": "Пороль проверен",
                },
                status=status.HTTP_200_OK,
            )

        except DjangoUnicodeDecodeError:
            return Response(
                {
                    "statusCode": 400,
                    "success": False,
                    "data": None,
                    "message": "Ссылка недействительна",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class SetNewPasswordAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def patch(self, request):
        uidb64 = request.data.get("uidb64")
        token = request.data.get("token")
        password = request.data.get("password")

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {
                        "statusCode": 400,
                        "success": False,
                        "data": None,
                        "message": "Ссылка недействительна",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(password)
            user.save()
            return Response(
                {
                    "statusCode": 200,
                    "success": True,
                    "data": None,
                    "message": "Пароль успешно изменён",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "statusCode": 400,
                    "success": False,
                    "data": None,
                    "message": f"Что-то пошло не так: {str(e)}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )















import urllib.parse
import requests

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from user_profile.models import Profile
from users.models import SocialOnboardingSession


User = get_user_model()


def set_auth_cookies(response, request, access_token, refresh_token):
    cookie_params = {
        "secure": True,
        "samesite": "None",
        "path": "/",
    }

    # ВАЖНО: если COOKIE_DOMAIN пустой, domain вообще не передаем
    cookie_domain = getattr(settings, "COOKIE_DOMAIN", None)

    if cookie_domain:
        cookie_params["domain"] = cookie_domain

    csrf_token = get_token(request)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=cookie_params["secure"],
        samesite=cookie_params["samesite"],
        max_age=60 * 60,
        path=cookie_params["path"],
        domain=cookie_params.get("domain"),
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=cookie_params["secure"],
        samesite=cookie_params["samesite"],
        max_age=60 * 60 * 24 * 7,
        path=cookie_params["path"],
        domain=cookie_params.get("domain"),
    )

    response.set_cookie(
        key="has_session",
        value="1",
        httponly=False,
        secure=cookie_params["secure"],
        samesite=cookie_params["samesite"],
        path=cookie_params["path"],
        domain=cookie_params.get("domain"),
    )

    response.set_cookie(
        key="csrftoken",
        value=csrf_token,
        httponly=False,
        secure=cookie_params["secure"],
        samesite=cookie_params["samesite"],
        path=cookie_params["path"],
        domain=cookie_params.get("domain"),
    )

    return response


def google_login_view(request):
    redirect_uri = "https://lawly.up.railway.app/users/google/callback/"

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account",
    }

    google_url = "https://accounts.google.com/o/oauth2/v2/auth"

    return redirect(f"{google_url}?{urllib.parse.urlencode(params)}")


def google_callback_view(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "No code"}, status=400)

    redirect_uri = "https://lawly.up.railway.app/users/google/callback/"

    token_response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        timeout=15,
    )

    tokens = token_response.json()

    if token_response.status_code != 200:
        return JsonResponse(tokens, status=400)

    google_access_token = tokens.get("access_token")

    if not google_access_token:
        return JsonResponse({"error": "No Google access token"}, status=400)

    userinfo_response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {google_access_token}"},
        timeout=15,
    )

    userinfo = userinfo_response.json()

    email = userinfo.get("email")

    if not email:
        return JsonResponse({"error": "No email"}, status=400)

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "first_name": userinfo.get("given_name", ""),
            "last_name": userinfo.get("family_name", ""),
            "agreementAccepted": True,
            "privacyPolicyAccepted": True,
        },
    )

    user.first_name = userinfo.get("given_name", user.first_name or "")
    user.last_name = userinfo.get("family_name", user.last_name or "")
    user.save(update_fields=["first_name", "last_name"])

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.first_name = user.first_name
    profile.last_name = user.last_name

    if hasattr(profile, "email"):
        profile.email = user.email
        profile.save()
    else:
        profile.save(update_fields=["first_name", "last_name"])

    social_session = SocialOnboardingSession.create(
        user=user,
        provider="google",
        ttl_minutes=10,
    )

    frontend_url = settings.FRONTEND_URL.rstrip("/")

    return redirect(
        f"{frontend_url}/auth/google/callback?social_session={social_session.session_id}"
    )


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def google_exchange_view(request):
    session_id = request.data.get("social_session")

    if not session_id:
        return Response(
            {
                "statusCode": 400,
                "success": False,
                "data": None,
                "message": "social_session is required",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        social_session = SocialOnboardingSession.objects.get(
            session_id=session_id,
            provider="google",
        )
    except SocialOnboardingSession.DoesNotExist:
        return Response(
            {
                "statusCode": 400,
                "success": False,
                "data": None,
                "message": "Invalid social session",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = social_session.user

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    csrf_token = get_token(request)

    response = Response(
        {
            "statusCode": 200,
            "success": True,
            "data": {
                "csrf_token": csrf_token,
                "redirect": "/chat",
            },
            "message": "Google auth completed",
        },
        status=status.HTTP_200_OK,
    )

    return set_auth_cookies(
        response=response,
        request=request,
        access_token=access_token,
        refresh_token=refresh_token,
    )