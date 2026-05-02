from django.shortcuts import redirect

ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"
ACCESS_MAX_AGE = 7*24*60*60
REFRESH_MAX_AGE = 7*24*60*60
COOKIE_SECURE = False
COOKIE_HTTPONLY = False
COOKIE_SAMESITE = "Lax"

class JWTResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if hasattr(request, "_jwt_access_token") and hasattr(request, "_jwt_refresh_token"):
            response = redirect(getattr(request, "_jwt_redirect_url", "/"))
            response.set_cookie(
                key=ACCESS_COOKIE_NAME,
                value=request._jwt_access_token,
                httponly=COOKIE_HTTPONLY,
                secure=COOKIE_SECURE,
                samesite=COOKIE_SAMESITE,
                max_age=ACCESS_MAX_AGE,
            )
            response.set_cookie(
                key=REFRESH_COOKIE_NAME,
                value=request._jwt_refresh_token,
                httponly=COOKIE_HTTPONLY,
                secure=COOKIE_SECURE,
                samesite=COOKIE_SAMESITE,
                max_age=REFRESH_MAX_AGE,
            )

        return response