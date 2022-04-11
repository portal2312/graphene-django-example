"""Django settings for project project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from os import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-@67a14^3n@0c83$5gt(a+hh%k&=)u@e1j==-pc^117--+5jiag"  # nosec B105
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # graphene-django
    # https://docs.graphene-python.org/projects/django/en/latest/installation/
    "graphene_django",
    # local apps
    "ingredients",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# https://docs.djangoproject.com/en/4.0/ref/settings/#language-code
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "ko-KR"

# https://docs.djangoproject.com/en/4.0/ref/settings/#time-zone
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIME_ZONE = "Asia/Seoul"

USE_I18N = True

# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-USE_TZ
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# graphene-django
# https://docs.graphene-python.org/projects/django/en/latest/installation/
# https://docs.graphene-python.org/projects/django/en/latest/settings/
GRAPHENE = {
    "MIDDLEWARE": [],
    "SCHEMA": "project.schema.schema",
    "SCHEMA_INDENT": 2,
    "SCHEMA_OUTPUT": "schema.graphql",
}

# https://docs.djangoproject.com/en/4.0/ref/settings/#media-root
MEDIA_ROOT = environ.get("MEDIA_ROOT", "media")

# https://docs.djangoproject.com/en/4.0/ref/settings/#media-url
MEDIA_URL = "/media/"
