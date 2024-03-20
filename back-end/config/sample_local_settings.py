SECRET_KEY = ''

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

GOOGLE_CLIENT_ID = '29522453275-mloh24dqtibhbb9d6mbh66vbts6ahslm.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URI = 'http://localhost:8000/google-auth/redirect/'