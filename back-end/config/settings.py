from pathlib import Path
import os
from config import local_settings
from celery.schedules import crontab
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = local_settings.SECRET_KEY

DEBUG = local_settings.DEBUG

ALLOWED_HOSTS = local_settings.ALLOWED_HOSTS

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Application definition
DJANGO_DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'graphene_django',
    'import_export',
    
]

LOCAL_APPS = [
    "accounts.apps.AccountsConfig",
    'education.apps.EducationConfig',
    'home.apps.HomeConfig',
    'admin_dashboard_panel.apps.dashboard_panelConfig',
    'dashboard_student.apps.DashboardStudentConfig',
    'dashboard_teacher.apps.DashboardTeacherConfig',
    'dashboard_educationalassistant.apps.DashboardEducationalAssistantConfig',
    'academic_events.apps.AcademicConfig',
]

INSTALLED_APPS = DJANGO_DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database -> Postgresql
# DATABASES = {
#   'default': {
#       'ENGINE': 'django.db.backends.postgresql_psycopg2',
#       'NAME': local_settings.DATABASE['NAME'],
#       'HOST': local_settings.DATABASE['HOST'],
#       'USER': local_settings.DATABASE['USER'],
#       'PASSWORD': local_settings.DATABASE['PASSWORD'],
#       'PORT': local_settings.DATABASE['PORT'],
#   }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
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


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

IMPORT_EXPORT_USE_TRANSACTIONS = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = '/static/'
STATIC_ROOT = './static_files/'

if DEBUG:
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication'
        )
    }
else:
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            'rest_framework.authentication.TokenAuthentication'
        )
    }
REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Education Management API',
    'DESCRIPTION': 'a project for managing universicty',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}



CORS_ORIGIN_ALLOW_ALL = True

# # Email Configurations
EMAIL_BACKEND = local_settings.Email_Configuration['EMAIL_BACKEND']
EMAIL_HOST = local_settings.Email_Configuration['EMAIL_HOST']
EMAIL_PORT = local_settings.Email_Configuration['EMAIL_PORT']
EMAIL_HOST_USER = local_settings.Email_Configuration['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = local_settings.Email_Configuration['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = local_settings.Email_Configuration['EMAIL_USE_TLS']
DEFAULT_FROM_EMAIL = 'mohammadbaharloo96@gmail.com'

GRAPHENE = {
  'SCHEMA': 'graphql_api.schema.schema'
}


# Loging 

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
        'level': 'WARNING',
    },
}


GOOGLE_CLIENT_ID = local_settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = local_settings.GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI = local_settings.GOOGLE_REDIRECT_URI



CELERY_BROKER_URL = 'amqp://localhost'

CELERY_BEAT_SCHEDULE = {
    'send-new-year-email': {
        'task': 'tasks.send_new_year_email',
        'schedule': crontab(day_of_month=1, month_of_year=1, hour=0, minute=0),  
    },
}