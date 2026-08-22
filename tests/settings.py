"""Minimal Django settings used by the test suite."""

SECRET_KEY = 'cmsplugin-poll-tests'
DEBUG = True
USE_TZ = True
SITE_ID = 1
ROOT_URLCONF = 'tests.urls'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'treebeard',
    'menus',
    'sekizai',
    'cms',
    'cmsplugin_poll',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

CMS_TEMPLATES = [('base.html', 'Base')]
CMS_CONFIRM_VERSION4 = True
LANGUAGE_CODE = 'en'
STATIC_URL = '/static/'
