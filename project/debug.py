"""Django debug settings for project project."""
import os

from .settings import *  # pylint: disable=wildcard-import, unused-wildcard-import

ALLOWED_HOSTS = ["*"]

DEBUG = True

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += [
    "debug_toolbar",
]

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#enabling-middleware
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configuring-internal-ips
INTERNAL_IPS = [
    "127.0.0.1",
]

# https://docs.graphene-python.org/projects/django/en/latest/debug/#installation
GRAPHENE["MIDDLEWARE"] = [
    "graphene_django.debug.DjangoDebugMiddleware",
    *GRAPHENE.get("MIDDLEWARE", [])
]

# https://docs.djangoproject.com/en/4.0/topics/logging/
LOGGING_ACTIVATE = False
if LOGGING_ACTIVATE:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": os.path.join(MEDIA_ROOT, "django-debug.log"),
            },
            "mail_admins": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }
