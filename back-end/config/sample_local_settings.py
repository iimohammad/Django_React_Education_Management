SECRET_KEY = '4v&(r8*_t%=!-+k1#us&c6!pp^juy(^7i@!by*2%5=zx1f_(tk'

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

USE_DEBUG_TOOLBAR = True
USE_SILK = True
