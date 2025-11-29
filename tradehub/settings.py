import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

# DEBUG from environment
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Render requirement
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, "localhost", "*"]
else:
    ALLOWED_HOSTS = ["*"]

# ======================================
# APPLICATIONS
# ======================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # Crispy
    "crispy_forms",
    "crispy_tailwind",

    # Local apps
    "accounts",
    "dashboard",
    "payments",
    "stockmanagement",
    "assets",
]

AUTH_USER_MODEL = "accounts.CustomUser"

# ======================================
# MIDDLEWARE
# ======================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # IMPORTANT for Render static
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tradehub.urls"

# ======================================
# TEMPLATES
# ======================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "dashboard.context_processors.site_settings_context",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tradehub.wsgi.application"

# ======================================
# DATABASE (NEON Postgres)
# ======================================
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# ======================================
# PASSWORD VALIDATION
# ======================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ======================================
# STATIC + MEDIA
# (Corrected for Render & Admin issue)
# ======================================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Only add STATICFILES_DIRS if folder exists
if os.path.isdir(os.path.join(BASE_DIR, "static")):
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    STATICFILES_DIRS = []

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ======================================
# LOGIN / LOGOUT Redirects
# ======================================
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_URL = "logout"
LOGOUT_REDIRECT_URL = "login"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ======================================
# TEMP MIGRATION KEY
# ======================================
TEMP_MIGRATE_KEY = os.environ.get("TEMP_MIGRATE_KEY")
