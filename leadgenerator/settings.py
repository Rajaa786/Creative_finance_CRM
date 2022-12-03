from pathlib import Path
import environ
from django.conf.locale.en import formats as en_formats
import django_heroku


env = environ.Env(DEBUG=(bool, False))

READ_DOT_ENV_FILE = env.bool("READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"


STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = "static_root"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_DIR = BASE_DIR / "media"


SECRET_KEY = env("SECRET_KEY")
# SECRET_KEY = "fdfdfdfdfdffd"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
# DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "account.apps.AccountConfig",
    "master.apps.MasterConfig",
    "HomeLoan.apps.HomeloanConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "home",
    "stronghold",
    "mathfilters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "stronghold.middleware.LoginRequiredMiddleware",
]


ROOT_URLCONF = "leadgenerator.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "leadgenerator.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {

    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DATABASES_NAME"),
        "USER": env("DATABASES_USER"),
        "PASSWORD": env("DATABASES_PASSWORD"),
        "HOST": env("DATABASES_HOST"),
        # "HOST": "localhost",
        "PORT": env("DATABASES_PORT"),
#         "NAME": 'django-test',
#         "USER": 'root',
#         "PASSWORD": '',
#         "HOST": "localhost",
#         "PORT": 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "account.CustomUser"


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-US"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

en_formats.DATE_FORMAT = "M d, Y"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


MEDIA_URL = "/media/"
MEDIA_ROOT = MEDIA_DIR

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/


# SMTP Configuration
# EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# # EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_HOST = 'smtp.gmail.com'
# # EMAIL_PORT = os.environ.get('EMAIL_PORT')
# EMAIL_PORT = 587
# # EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
# # EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
# EMAIL_USE_TLS = True
# # EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_USER = 'vinayjain449@gmail.com'
# # EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# EMAIL_HOST_PASSWORD = 'rzvujwqswaduhgih'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'rajsingh08471@gmail.com'
EMAIL_HOST_PASSWORD = 'rzvujwqswaduhgih'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


django_heroku.settings(locals())



LOGIN_URL = "/account/login"

# https://github.com/mgrouchy/django-stronghold

# STRONGHOLD_DEFAULTS = env('STRONGHOLD_DEFAULTS')
STRONGHOLD_PUBLIC_NAMED_URLS = (
    "home",
    "register",
    "forgot_username",
    "reset_password",
    "password_reset_done",
    "password_reset_confirm",
    "password_reset_complete",
)
STRONGHOLD_PUBLIC_URLS = ("/admin/",)

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = "DENY"

    ALLOWED_HOSTS = ["*"]
