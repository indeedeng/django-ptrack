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

# django-webtest package requires SessionMiddleware and AuthenticationMiddleware
MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
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
