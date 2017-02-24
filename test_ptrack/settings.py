# encoding: utf-8

import os

# DJANGO TEST SETTINGS
SECRET_KEY = 'ptracktestsecret'
STATIC_URL = '/'

# Is this required?
# ROOT_URLCONF = 'ptrack.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'ptrack_test.db',
    }
}


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'ptrack'
]

ROOT_URLCONF = 'ptrack.urls'

# Default classes plus SessionMiddleware and AuthenticationMiddleware
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }
]

ALLOWED_HOSTS = ['localhost']


# PTRACK SETTINGS

PTRACK_SECRET = 'testptracksecret'
PTRACK_APP_URL = 'localhost'
USE_AES = True
