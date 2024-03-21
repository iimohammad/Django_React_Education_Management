SECRET_KEY = ''

# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': '<db_name>',
      'HOST': 'localhost',
      'USER': '<db_username>',
      'PASSWORD': '<password>',
      'PORT': '<db_port>',
  }
}

Email_Configuration = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'smtp.gmail.com',
    'EMAIL_PORT': 587,
    'EMAIL_HOST_USER': '"',
    'EMAIL_HOST_PASSWORD': '',
    'EMAIL_USE_TLS': True,
    'EMAIL_USE_SSL': False
}

Admin = 'adminMohammad/'

GOOGLE_CLIENT_ID = '29522453275-mloh24dqtibhbb9d6mbh66vbts6ahslm.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URI = 'http://localhost:8000/google-auth/redirect/'