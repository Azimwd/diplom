from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from users.models import Users
from django.middleware.csrf import CsrfViewMiddleware


class CookieAuthentication(BaseAuthentication):

    def enforce_csrf(self, request):
        
        csrf_middleware = CsrfViewMiddleware(lambda req: None)
        result = csrf_middleware.process_view(request, None, (), {})
        if result is not None:
            raise AuthenticationFailed("CSRF validation failed")

    def authenticate(self, request):
        token = request.COOKIES.get("access_token")
        print("COOKIES:", request.COOKIES)
        print("METHOD:", request.method)
        print("X-CSRFToken:", request.headers.get("X-CSRFToken"))
        print("CSRF cookie:", request.COOKIES.get("csrftoken"))

        if not token:
            return None

        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            self.enforce_csrf(request)

        try:
            access = AccessToken(token)
            user = Users.objects.get(id=access["user_id"])
            return (user, None)

        except Users.DoesNotExist:
            raise NotAuthenticated("User not found")
        except TokenError:
            raise NotAuthenticated("Invalid or expired access token")
        except Exception as e:
            raise NotAuthenticated(f"Authentication error: {str(e)}")