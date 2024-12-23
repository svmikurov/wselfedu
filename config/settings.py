"""Django settings module."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv('./.env_vars/.env')

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = bool(os.getenv('DEBUG'))
ENVIRONMENT = os.getenv('ENVIRONMENT')
PAGINATION_SIZE = int(os.getenv('PAGINATION_SIZE', 20))

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '77.222.53.52',
    'wselfedu.online',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # added django apps
    'django.contrib.admindocs',
    # installed packages
    'django_extensions',
    'django_bootstrap5',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    # https://django-simple-captcha.readthedocs.io/en/latest/usage.html
    'captcha',
    # added apps
    'users.apps.UsersConfig',
    'foreign.apps.ForeignConfig',
    'mathematics.apps.MathematicsConfig',
    'glossary.apps.GlossaryConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # added
                'config.context_processor.pass_var_to_template',
                'users.context_processors.add_student_user_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASS'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

AUTH_USER_MODEL = 'users.UserApp'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa: E501
    },
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Yekaterinburg'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_src'),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
# End Static files

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Bootstrap
# https://pypi.org/project/crispy-bootstrap5/
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
# End Bootstrap


# Django’s cache framework
# https://docs.djangoproject.com/en/5.0/topics/cache/#django-s-cache-framework
# Redis
# https://docs.djangoproject.com/en/5.0/topics/cache/#redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379',
    }
}


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}  # End Logging


# Django REST framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    # https://www.django-rest-framework.org/api-guide/pagination/#setting-the-pagination-style
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',  # noqa: E501
    'PAGE_SIZE': PAGINATION_SIZE,
}

FIXTURE_DIRS = ['tests/fixtures/']


# Captcha
# https://django-simple-captcha.readthedocs.io/en/latest/advanced.html#captcha-test-mode
# https://stackoverflow.com/questions/3159284/how-to-unit-test-a-form-with-a-captcha-field-in-django
if ENVIRONMENT == 'development':
    CAPTCHA_TEST_MODE = True

# Djoser authentication
DJOSER = {
    # https://djoser.readthedocs.io/en/latest/settings.html#permissions
    'PERMISSIONS': {
        # Admin only
        'activation': ['rest_framework.permissions.IsAdminUser'],
        'password_reset': ['rest_framework.permissions.IsAdminUser'],
        'password_reset_confirm': ['rest_framework.permissions.IsAdminUser'],
        'set_password': ['djoser.permissions.IsAdminUser'],
        'username_reset': ['rest_framework.permissions.IsAdminUser'],
        'username_reset_confirm': ['rest_framework.permissions.IsAdminUser'],
        'set_username': ['djoser.permissions.IsAdminUser'],
        'user_create': ['rest_framework.permissions.IsAdminUser'],
        'user_delete': ['djoser.permissions.IsAdminUser'],
        'user_list': ['djoser.permissions.IsAdminUser'],
        # Allowed
        'user': ['djoser.permissions.CurrentUserOrAdmin'],
        'token_create': ['rest_framework.permissions.AllowAny'],
        'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    },
}
