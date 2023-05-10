"""
Django settings for WadiMedicalCenter project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url
import environ
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#env = environ.Env()

#environ.Env.read_env()
load_dotenv()  #load env vars
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d#v$@0g^o0_^of=^7v5&0_$@nia&@br$zjp&o0d(dc1$l37cir'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "account.apps.AccountConfig",
    "appointment.apps.AppointmentConfig",
    "patient.apps.PatientConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    # 'django_extensions',
]
# GRAPH_MODELS ={
# 'all_applications': True,
# 'graph_models': True,
# }
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
       
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.permissions.IsAuthenticated',
    )    
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
#CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = ['chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop']

# ALLOWED_HOSTS = ["your-domain.herokuapp.com",
#                  "chrome-extension://theIDofYourExtension"]
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:8000',
# ]


ROOT_URLCONF = "WadiMedicalCenter.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR,'templates'],
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

WSGI_APPLICATION = "WadiMedicalCenter.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


#     #    {
#     #  "default": dj_database_url.parse(
#     #     os.environ.get("DATABASE_URL")
#     #  )


# To use Neon with Django, you have to create a Project on Neon and specify the project connection settings in your settings.py in the same way as for standalone Postgres.

DATABASES = {
  'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
   
   
 }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Asia/Damascus'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#MEDIA
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'


AUTH_USER_MODEL = "account.User"
