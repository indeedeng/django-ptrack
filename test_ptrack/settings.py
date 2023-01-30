"""Settings for ptrack tests."""
SECRET_KEY = "ptracktestsecret"  # nosec B105
STATIC_URL = "/"

# Is this required?
# ROOT_URLCONF = 'ptrack.urls'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "ptrack_test.db",
    }
}

INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "django.contrib.staticfiles", "ptrack"]

ROOT_URLCONF = "ptrack.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]

ALLOWED_HOSTS = ["localhost"]

# PTRACK SETTINGS

PTRACK_SECRET = "testptracksecret"  # nosec B105
PTRACK_APP_URL = "localhost"
USE_AES = True
