"""Django settings for wselfedu project."""

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

from utils.load import getenv_bool

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

PRODUCTION = getenv_bool('PRODUCTION')

DEBUG = getenv_bool('DEBUG')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Installed apps
    'rest_framework',
    'rest_framework_simplejwt',
    # Django extensions
    'django_extensions',
    # Documentation
    'drf_spectacular',
    # layout
    'django_bootstrap5',
    'crispy_forms',
    'crispy_bootstrap5',
    # Applications
    'apps.main',
    'apps.users',
    'apps.math',
    'apps.lang',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wselfedu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# WSGI

WSGI_APPLICATION = 'wselfedu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://username:password@localhost:5432/dbname',
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = 'login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django REST framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # djangorestframework-simplejwt
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Pagination
    # https://www.django-rest-framework.org/tutorial/quickstart/#pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # REST API documentation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


# Djoser authentication

DJOSER = {
    # https://djoser.readthedocs.io/en/latest/settings.html#permissions
    'PERMISSIONS': {
        'user_list': ['rest_framework.permissions.IsAdminUser'],
    },
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}


# REST API documentation
# https://drf-spectacular.readthedocs.io/en/latest/readme.html#installation

SPECTACULAR_SETTINGS = {
    'TITLE': 'WSE Django and REST backend',
    'DESCRIPTION': 'WSE Series site',
    'VERSION': '0.7.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}


# Graph models
# https://django-extensions.readthedocs.io/en/latest/graph_models.html


GRAPH_MODELS = {
    'app_labels': [
        'lang',
        'main',
        'math',
        'users',
    ],
    'exclude_models': [
        'AbstractBaseSession',
        'AbstractUser',
        'Group',
        'LogEntry',
        'Permission',
        'Session',
    ],
    'rankdir': 'TB',  # Direction of the diagram (TB, LR, BT, RL)
    'arrow_shape': 'normal',  # ['box', 'crow', 'curve', 'icurve', 'diamond', 'dot', 'inv', 'none', 'normal', 'tee', 'vee',]
}


LOGGING_ON = getenv_bool('LOGGING')

if LOGGING_ON:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'sql': {
                '()': 'utils.reports.formatters.sql.simple.SimpleSQLFormatter',
            },
        },
        'handlers': {
            'sql_console': {
                'level': 'DEBUG',
                'class': 'utils.reports.formatters.sql.third_party.ColorfulSQLHandler',
                'formatter': 'sql',
            },
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['sql_console'],
                'propagate': False,
            },
        },
    }
