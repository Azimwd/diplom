# import requests
# from rest_framework.views import APIView, Response
# from users.serializers import *
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# from rest_framework.permissions import AllowAny
# from django.http import JsonResponse
# from django.shortcuts import redirect
# from rest_framework import generics, status
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ObjectDoesNotExist
# from django.middleware.csrf import get_token
# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

# ACCESS_COOKIE_NAME = "access_token"
# REFRESH_COOKIE_NAME = "refresh_token"
# ACCESS_MAX_AGE = 7*24*60*60
# REFRESH_MAX_AGE = 7*24*60*60
# COOKIE_SECURE = False
# COOKIE_HTTPONLY = False
# COOKIE_SAMESITE = "Lax"

# User = get_user_model()

# @ensure_csrf_cookie
# def csrf_token_view(request):
#     return JsonResponse({'csrf_token': get_token(request)})

# class Registrations(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)

#         if serializer.is_valid():
#             user = serializer.save()

#             return Response({
#                  "user_id": user.id,
#                 "message": "Регистрация завершена"
#             }, status=status.HTTP_201_CREATED)
        
#         errors = serializer.errors

#         def get_first_error(errs):
#             if isinstance(errs, list) and errs:
#                 return str(errs[0])
#             elif isinstance(errs, dict) and errs:
#                 return get_first_error(next(iter(errs.values())))
#             return None

#         first_error = get_first_error(errors)

#         return Response({
#             "message": first_error or "Ошибка валидации"
#         }, status=status.HTTP_400_BAD_REQUEST)
    

# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data['user']

#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         refresh_token = str(refresh)

#         response = Response({
#             "id": user.id,
#             "email": user.email,
#             "role": getattr(user, "role", None),
#             "csrf_token": get_token(request),
#             "message": "Успешный вход"
#         }, status=status.HTTP_200_OK)

#         response.set_cookie(
#             key=ACCESS_COOKIE_NAME,
#             value=access_token,
#             httponly=COOKIE_HTTPONLY,
#             secure=COOKIE_SECURE,
#             samesite=COOKIE_SAMESITE,
#             max_age=ACCESS_MAX_AGE,
#         )
#         response.set_cookie(
#             key=REFRESH_COOKIE_NAME,
#             value=refresh_token,
#             httponly=COOKIE_HTTPONLY,
#             secure=COOKIE_SECURE,
#             samesite=COOKIE_SAMESITE,
#             max_age=REFRESH_MAX_AGE,
#         )

#         return response


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)

#         response = Response({
#             "message": "Успешный выход"
#         }, status=status.HTTP_200_OK)

#         if refresh_token:
#             try:
#                 token = RefreshToken(refresh_token)
#                 token.blacklist()
#             except TokenError:
#                 pass

#         response.delete_cookie(ACCESS_COOKIE_NAME)
#         response.delete_cookie(REFRESH_COOKIE_NAME)

#         if request.user.socialaccount_set.filter(provider="google").exists():
#             google_logout_url = (
#                 "https://accounts.google.com/Logout?continue="
#                 "https://appengine.google.com/_ah/logout?continue=http://localhost:3000/"
#             )
#             return redirect(google_logout_url)

#         return response
        

# @method_decorator(csrf_exempt, name='dispatch')
# class TokenRefreshView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []
#     def post(self, request):
#         refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)
#         if not refresh_token:
#             return Response({
#                 "message": "Отсутствует refresh token"
#             }, status=status.HTTP_401_UNAUTHORIZED)

#         try:
#             refresh = RefreshToken(refresh_token)
#         except TokenError:
#             return Response({
#                 "message": "Refresh token недействителен или просрочен"
#             }, status=status.HTTP_401_UNAUTHORIZED)

#         user_id = refresh.get("user_id")
#         try:
#             user = User.objects.get(id=user_id)
#         except ObjectDoesNotExist:
#             return Response({
#                 "message": "Пользователь не найден"
#             }, status=status.HTTP_401_UNAUTHORIZED)

#         try:
#             refresh.blacklist()
#         except (AttributeError, TokenError):
#             pass

#         new_refresh = RefreshToken.for_user(user)
#         new_access = str(new_refresh.access_token)
#         new_refresh_token = str(new_refresh)

#         response = Response({
#             "message": "Access token обновлён",
#         }, status=status.HTTP_200_OK)

#         response.set_cookie(
#             key=ACCESS_COOKIE_NAME,
#             value=new_access,
#             httponly=COOKIE_HTTPONLY,
#             secure=COOKIE_SECURE,
#             samesite=COOKIE_SAMESITE,
#             max_age=ACCESS_MAX_AGE,
#         )
#         response.set_cookie(
#             key=REFRESH_COOKIE_NAME,
#             value=new_refresh_token,
#             httponly=COOKIE_HTTPONLY,
#             secure=COOKIE_SECURE,
#             samesite=COOKIE_SAMESITE,
#             max_age=REFRESH_MAX_AGE,
#         )

#         return response


# class UserInfoView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
       
#         user = request.user
#         response = Response({
#             "id": user.id,
#             "email": user.email,
#             "role": user.role,
#             "message": "Успешный вход"
#         }, status=status.HTTP_200_OK)

#         return response


# class RequestPasswordResetEmail(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         email = request.data.get('email')
#         user = User.objects.filter(email=email).first()
#         if user:
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             reset_url = f"http://localhost:8000/auth/reset-password-confirm/{uidb64}/{token}/"
#             send_mail(
#                 subject="Сброс пароля",
#                 message=f"Перейдите по ссылке, чтобы сбросить пароль: {reset_url}",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[email],
#                 fail_silently=False
#             )

#         return Response({
#                 "message": "На вашу почту была отправлена ссылка для восстановления пароля",
#                 "uidb64": uidb64,
#                 "token": token,
#                 }, status=status.HTTP_200_OK)


# class PasswordTokenCheckAPI(generics.GenericAPIView):
#     def get(self, request, uidb64, token):
#         try:
#             user_id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=user_id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({
#                     "message": "Ссылка недействительна"
#                     }, status=status.HTTP_400_BAD_REQUEST)
#             return Response({
#                     'uidb64': uidb64, 
#                     'token': token,
#                     "message": "Пороль проверен"
#                     }, status=status.HTTP_200_OK)
        
#         except DjangoUnicodeDecodeError:
#             return Response({
#                     "message": "Ссылка недействительна"
#                     }, status=status.HTTP_400_BAD_REQUEST)


# class SetNewPasswordAPIView(generics.GenericAPIView):
#     def patch(self, request):
#         uidb64 = request.data.get('uidb64')
#         token = request.data.get('token')
#         password = request.data.get('password')

#         try:
#             user_id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=user_id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({
#                     "message": "Ссылка недействительна"
#                     }, status=status.HTTP_400_BAD_REQUEST)
#             user.set_password(password)
#             user.save()
#             return Response({
#                 "message": "Пароль успешно изменён"
#                 }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({
#                 "message": f"Что-то пошло не так: {str(e)}"
#             }, status=status.HTTP_400_BAD_REQUEST)

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

ACCESS_MAX_AGE = 15 * 60
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
    
def google_callback_view(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "No code"}, status=400)

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": "https://lawly.up.railway.app/accounts/google/login/callback/",
        "grant_type": "authorization_code",
    }
    r = requests.post(token_url, data=data, timeout=15)
    tokens = r.json()
    if "error" in tokens:
        return JsonResponse(tokens, status=400)

    userinfo = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {tokens['access_token']}"} ,
        timeout=15,
    ).json()

    email = userinfo.get("email")
    if not email:
        return JsonResponse({"error": "No email"}, status=400)

    user, created = User.objects.get_or_create(email=email)

    # обнови имена (если есть)
    user.first_name = userinfo.get("given_name", user.first_name or "")
    user.last_name = userinfo.get("family_name", user.last_name or "")
    user.save(update_fields=["first_name", "last_name"])

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.first_name = user.first_name
    profile.last_name = user.last_name
    profile.email = user.email
    profile.save()

    if created or not getattr(user, "role", None):
        s = SocialOnboardingSession.create(user=user, provider="google", ttl_minutes=10)
        return redirect(
            f"https://lawly.up.railway.app/auth/choose-role?social_session={s.session_id}"
        )

    refresh = RefreshToken.for_user(user)
    response = redirect("http://localhost:5173")

    response.set_cookie(
        ACCESS_COOKIE_NAME,
        str(refresh.access_token),
        httponly=COOKIE_HTTPONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=ACCESS_MAX_AGE,
        path="/",
        domain=COOKIE_DOMAIN,
    )

    response.set_cookie(
        REFRESH_COOKIE_NAME,
        str(refresh),
        httponly=COOKIE_HTTPONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=REFRESH_MAX_AGE,
        path="/",
        domain=COOKIE_DOMAIN,
    )

    response.set_cookie(
        SESSION_FLAG_COOKIE,
        "1",
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
                "statusCode": 200,
                "success": True,
                "data": {
                    "id": user.id,
                    "email": user.email,
                    "role": getattr(user, "role", None),
                    "csrf_token": csrf_token,
                },
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
            resp = Response(
                {"detail": "No session"}, status=status.HTTP_401_UNAUTHORIZED
            )
            clear_auth_cookies(resp)
            return resp

        try:
            RefreshToken(refresh)
            return Response({"ok": True}, status=status.HTTP_200_OK)
        except TokenError:
            resp = Response(
                {"detail": "Session expired"}, status=status.HTTP_401_UNAUTHORIZED
            )
            clear_auth_cookies(resp)
            return resp


def clear_auth_cookies(response: HttpResponse) -> HttpResponse:
    response.delete_cookie(ACCESS_COOKIE_NAME, path="/", domain=COOKIE_DOMAIN)
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/", domain=COOKIE_DOMAIN)
    response.delete_cookie(SESSION_FLAG_COOKIE, path="/", domain=COOKIE_DOMAIN)
    response.delete_cookie("csrftoken", path="/", domain=COOKIE_DOMAIN)
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

        try:
            if (
                getattr(request.user, "is_authenticated", False)
                and request.user.socialaccount_set.filter(provider="google").exists()
            ):
                google_logout_url = (
                    "https://accounts.google.com/Logout?continue="
                    "https://appengine.google.com/_ah/logout?continue=http://localhost:5173"
                )
                redirect_response = redirect(google_logout_url)
                clear_auth_cookies(redirect_response)
                return redirect_response
        except Exception:
            pass

        return response


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        old_refresh = request.COOKIES.get(REFRESH_COOKIE_NAME)
        if not old_refresh:
            resp = Response(
                {"detail": "No refresh"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            clear_auth_cookies(resp)
            return resp

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

        resp = Response({"success": True}, status=status.HTTP_200_OK)

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
                "statusCode": 200,
                "success": True,
                "data": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
                "message": "Успешный вход",
            },
            status=status.HTTP_200_OK,
        )

        return response


# class EmailVerifyView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def get(self, request):
#         token = request.query_params.get("token")

#         try:
#             session = RegistrationSession.objects.get(email_verification_token=token)
#         except RegistrationSession.DoesNotExist:
#             return redirect("https://www.yurgid.kz/verify-email?status=invalid")

#         if session.is_email_verified:
#             return redirect(
#                 "https://www.yurgid.kz/verify-email?status=already_verified"
#             )

#         session.is_email_verified = True
#         session.save()

#         return redirect("https://www.yurgid.kz/verify-email?status=success")


# class ResendVerificationEmailView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def post(self, request):
#         email = request.data.get("email")
#         session = RegistrationSession.objects.filter(email=email).first()

#         if not session:
#             return Response({"message": "Сессия не найдена"}, status=404)

#         if session.is_email_verified:
#             return Response({"message": "Email уже подтверждён"}, status=400)

#         if session.last_email_sent_at:
#             if timezone.now() - session.last_email_sent_at < timedelta(seconds=60):
#                 return Response(
#                     {"message": "Повторная отправка возможна через минуту"},
#                     status=429,
#                 )

#         verification_url = (
#             f"https://diplom-production-db9e.up.railway.app/api/users/verify-email?"
#             f"token={session.email_verification_token}"
#         )

#         try:
#             resend_verification_email(session.email, verification_url)
#         except requests.RequestException as e:
#             return Response(
#                 {"message": f"Ошибка отправки письма: {str(e)}"},
#                 status=500,
#             )

#         session.last_email_sent_at = timezone.now()
#         session.save(update_fields=["last_email_sent_at"])

#         return Response(
#             {"success": True, "message": "Письмо отправлено повторно"},
#             status=200,
#         )


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
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = (
                f"http://localhost:5173/auth/reset-password-confirm/{uidb64}/{token}/"
            )

            try:
                send_password_reset_email(email, reset_url)
            except requests.RequestException as e:
                return Response(
                    {
                        "statusCode": 500,
                        "success": False,
                        "data": None,
                        "message": f"Ошибка отправки письма: {str(e)}",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {
                "statusCode": 200,
                "success": True,
                "data": None,
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
