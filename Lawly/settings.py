from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


# =========================
# MAIN SETTINGS
# =========================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-local-dev-key-only"
    else:
        raise RuntimeError("SECRET_KEY environment variable is required")
    
DEBUG = env_bool("DEBUG", False)

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://diplom-production-db9e.up.railway.app"
).rstrip("/")

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
).rstrip("/")

ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    "diplom-production-db9e.up.railway.app,localhost,127.0.0.1"
)

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    f"{BACKEND_URL},{FRONTEND_URL},http://localhost:5173,http://127.0.0.1:5173"
)

CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS",
    f"{FRONTEND_URL},http://localhost:5173,http://127.0.0.1:5173"
)

CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["Set-Cookie"]


# =========================
# COOKIE SETTINGS
# =========================

ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"
SESSION_FLAG_COOKIE = "has_session"

ACCESS_MAX_AGE = 15 * 60
REFRESH_MAX_AGE = 30 * 24 * 60 * 60

COOKIE_SECURE = env_bool("COOKIE_SECURE", True)
COOKIE_HTTPONLY = env_bool("COOKIE_HTTPONLY", True)
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "None")

_raw_cookie_domain = os.getenv("COOKIE_DOMAIN", "")
COOKIE_DOMAIN = _raw_cookie_domain if _raw_cookie_domain else None

SESSION_COOKIE_SECURE = COOKIE_SECURE
CSRF_COOKIE_SECURE = COOKIE_SECURE

SESSION_COOKIE_SAMESITE = COOKIE_SAMESITE
CSRF_COOKIE_SAMESITE = COOKIE_SAMESITE

CSRF_COOKIE_HTTPONLY = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",

    "users.apps.UsersConfig",
    "user_profile.apps.UserProfileConfig",
    "settings.apps.SettingsConfig",
    "chats",
    "subscriptions",
    "payments",
    "telegram_bot",
    "ai_documents",
    "ai_modules",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    "corsheaders",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "allauth.account.middleware.AccountMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middleware.JWTResponseMiddleware",
]

ROOT_URLCONF = "Lawly.urls"
WSGI_APPLICATION = "Lawly.wsgi.application"


# =========================
# DATABASE
# =========================

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}


# =========================
# USER / AUTH
# =========================

AUTH_USER_MODEL = "users.Users"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"

SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "offline",
            "prompt": "select_account",
        },
    }
}


# =========================
# GOOGLE OAUTH
# =========================

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

GOOGLE_OAUTH_CALLBACK_URL = os.getenv(
    "GOOGLE_OAUTH_CALLBACK_URL",
    f"{BACKEND_URL}/accounts/google/login/callback/"
)

LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", f"{FRONTEND_URL}/")


# =========================
# EMAIL / RESEND
# =========================

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "YurGid <noreply@yurgid.kz>")


# =========================
# PAYMENTS
# =========================

ROBOKASSA_LOGIN = os.getenv("ROBOKASSA_LOGIN", "")
ROBOKASSA_PASSWORD1 = os.getenv("ROBOKASSA_PASSWORD1", "")
ROBOKASSA_PASSWORD2 = os.getenv("ROBOKASSA_PASSWORD2", "")
ROBOKASSA_TEST_MODE = env_bool("ROBOKASSA_TEST_MODE", True)


# =========================
# TELEGRAM
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


# =========================
# CELERY / REDIS
# =========================

REDIS_URL = os.getenv("REDIS_URL", "")

CELERY_BROKER_URL = REDIS_URL or "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = REDIS_URL or "redis://localhost:6379/0"

CELERY_BEAT_SCHEDULE = {
    "refresh-tokens-every-month": {
        "task": "users.tasks.monthly_tokens_refresh",
        "schedule": crontab(minute=0, hour=0, day_of_month=1),
    },
}


# =========================
# REST FRAMEWORK
# =========================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "users.authentication.CookieAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": [
        "utils.response.APIRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "EXCEPTION_HANDLER": "core.exception_handler.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "BLACKLIST_AFTER_ROTATION": True,
    "ROTATE_REFRESH_TOKENS": True,
}


# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =========================
# LANGUAGE / TIME
# =========================

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_TZ = True


# =========================
# STATIC / MEDIA
# =========================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# STORAGES 
# =========================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}