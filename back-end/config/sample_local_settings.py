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