from rest_framework.views import APIView, Response
from users.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import generics, status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie


ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"
ACCESS_MAX_AGE = 7*24*60*60
REFRESH_MAX_AGE = 7*24*60*60
COOKIE_SECURE = False
COOKIE_HTTPONLY = False
COOKIE_SAMESITE = "Lax"

User = get_user_model()

@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({'csrf_token': get_token(request)})

class Registrations(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                "statusCode": 201,
                "success": True,
                "data": {
                    "user_id": user.id
                },
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
            "statusCode": 400,
            "success": False,
            "data": None,
            "message": first_error or "Ошибка валидации"
        }, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            "statusCode": 200,
            "success": True,
            "data": {
                "id": user.id,
                "email": user.email,
                "role": getattr(user, "role", None),
                "csrf_token": get_token(request)
            },
            "message": "Успешный вход"
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key=ACCESS_COOKIE_NAME,
            value=access_token,
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=ACCESS_MAX_AGE,
        )
        response.set_cookie(
            key=REFRESH_COOKIE_NAME,
            value=refresh_token,
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=REFRESH_MAX_AGE,
        )

        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)

        response = Response({
            "statusCode": 200,
            "success": True,
            "data": None,
            "message": "Успешный выход"
        }, status=status.HTTP_200_OK)

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        response.delete_cookie(ACCESS_COOKIE_NAME)
        response.delete_cookie(REFRESH_COOKIE_NAME)

        # if request.user.socialaccount_set.filter(provider="google").exists():
        #     google_logout_url = (
        #         "https://accounts.google.com/Logout?continue="
        #         "https://appengine.google.com/_ah/logout?continue=http://localhost:3000/"
        #     )
        #     return redirect(google_logout_url)

        return response
        
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)
        if not refresh_token:
            return Response({
                "statusCode": 401,
                "success": False,
                "data": None,
                "message": "Отсутствует refresh token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            return Response({
                "statusCode": 401,
                "success": False,
                "data": None,
                "message": "Refresh token недействителен или просрочен"
            }, status=status.HTTP_401_UNAUTHORIZED)

        user_id = refresh.get("user_id")
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({
                "statusCode": 401,
                "success": False,
                "data": None,
                "message": "Пользователь не найден"
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh.blacklist()
        except (AttributeError, TokenError):
            pass

        new_refresh = RefreshToken.for_user(user)
        new_access = str(new_refresh.access_token)
        new_refresh_token = str(new_refresh)

        response = Response({
            "statusCode": 200,
            "success": True,
            "data": None,
            "message": "Access token обновлён",
            "csrf_token": get_token(request)
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key=ACCESS_COOKIE_NAME,
            value=new_access,
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=ACCESS_MAX_AGE,
        )
        response.set_cookie(
            key=REFRESH_COOKIE_NAME,
            value=new_refresh_token,
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=REFRESH_MAX_AGE,
        )

        return response

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
       
        user = request.user
        response = Response({
            "statusCode": 200,
            "success": True,
            "data": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            },
            "message": "Успешный вход"
        }, status=status.HTTP_200_OK)

        return response

class RequestPasswordResetEmail(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = f"http://localhost:8000/auth/reset-password-confirm/{uidb64}/{token}/"
            send_mail(
                subject="Сброс пароля",
                message=f"Перейдите по ссылке, чтобы сбросить пароль: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )

        return Response({
                    "statusCode": 200,
                    "success": True,
                    "data": None,
                    "message": "На вашу почту была отправлена ссылка для восстановления пароля"
                    }, status=status.HTTP_200_OK)


User = get_user_model()
class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    "statusCode": 400,
                    "success": False,
                    "data": None,
                    "message": "Ссылка недействительна"
                    }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                        "statusCode": 200,
                        "success": True,
                        "data": {'uidb64': uidb64, 'token': token},
                        "message": "Пороль проверен"
                        }, status=status.HTTP_200_OK)
        
        except DjangoUnicodeDecodeError:
            return Response({
                    "statusCode": 400,
                    "success": False,
                    "data": None,
                    "message": "Ссылка недействительна"
                    }, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(generics.GenericAPIView):
    def patch(self, request):
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        password = request.data.get('password')

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    "statusCode": 400,
                    "success": False,
                    "data": None,
                    "message": "Ссылка недействительна"
                    }, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
            return Response({
                            "statusCode": 200,
                            "success": True,
                            "data": None,
                            "message": "Пароль успешно изменён"
                            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "statusCode": 400,
                "success": False,
                "data": None,
                "message": f"Что-то пошло не так: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

