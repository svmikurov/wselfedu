"""Django settings for wselfedu project."""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

from utils.load import get_boolean_value

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DJANGO_ENV = os.getenv('DJANGO_ENV')
PRODUCTION = DJANGO_ENV in {'production'}

DEBUG = get_boolean_value('DEBUG')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

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
    'crispy_bootstrap5',
    'crispy_forms',
    'django_bootstrap5',
    'django_htmx',
    'django_filters',
    'django_extensions',
    'drf_spectacular',
    # Applications
    'apps.core',
    'apps.glossary',
    'apps.lang',
    'apps.math',
    'apps.study',
    'apps.users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Internationalization
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # https://django-htmx.readthedocs.io/en/latest/installation.html#id1
    'django_htmx.middleware.HtmxMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    # Add 'debug_toolbar' to `INSTALLED_APPS` & `MIDDLEWARE`
    try:
        app_index = INSTALLED_APPS.index('django.contrib.staticfiles')
        INSTALLED_APPS.insert(app_index + 1, 'debug_toolbar')
    except ValueError:
        INSTALLED_APPS.append('debug_toolbar')

    middleware = 'debug_toolbar.middleware.DebugToolbarMiddleware'
    session_middleware = 'django.contrib.sessions.middleware.SessionMiddleware'
    try:
        middleware_index = MIDDLEWARE.index('django.contrib.staticfiles')
        MIDDLEWARE.insert(middleware_index, middleware)
    except ValueError:
        try:
            session_index = MIDDLEWARE.index(session_middleware)
            MIDDLEWARE.insert(session_index + 1, middleware)
        except ValueError:
            MIDDLEWARE.insert(1, middleware)

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
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
    }
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

AUTH_USER_MODEL = 'users.Person'

LOGIN_URL = '/login'
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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_src'),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django REST framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # Pagination
    # https://www.django-rest-framework.org/tutorial/quickstart/#pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # REST API documentation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Custom render
    'DEFAULT_RENDER_CLASSES': [
        'apps.core.api.v1.renders.WrappedJSONRenderer',
    ],
    'EXCEPTION_HANDLER': 'apps.core.exceptions.handler.custom_exception_handler',
}


# Djoser authentication

DJOSER = {
    # https://djoser.readthedocs.io/en/latest/settings.html#permissions
    'PERMISSIONS': {
        'user_list': ['rest_framework.permissions.IsAdminUser'],
    },
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}


# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'


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
        'core',
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


LOGGING_ON = get_boolean_value('LOGGING')

if LOGGING_ON:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'sql': {
                '()': 'utils.logger.formatters.simple.SimpleSQLFormatter',
            },
        },
        'handlers': {
            'sql_console': {
                'level': 'DEBUG',
                'class': 'utils.logger.handlers.third_party.ColorfulSQLHandler',
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

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    'IS_RUNNING_TESTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
    'RENDER_PANELS': True,
    'INSERT_BEFORE': '</body>',
}

# --------------------
# Internationalization
# --------------------

# Enable i18n
USE_I18N = True

# Supported languages
LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
    ('nl', 'Nederlands'),
]

# Default language
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en')

# Path to translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
