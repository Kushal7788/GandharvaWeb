"""
Django settings for GandharvaWeb19 project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^)ef3%8r$&327z%qz92yxgcxt6m@4s8j7$czx%5r6140^zh&g4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'gandharva19.pythonanywhere.com', '0.0.0.0', 'localhost', 'www.viitgandharva.com',
                 'viitgandharva.com', '*.viitgandharva.com', '192.168.43.139', '192.168.43.211']

# Application definition

INSTALLED_APPS = [
    'GandharvaWeb19',
    'EventApp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'sweetify'
]
AUTH_USER_MODEL = 'EventApp.MyUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GandharvaWeb19.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'EventApp.context_processors.add_variable_to_context',
            ],
        },
    },
]
AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    'social_core.backends.github.GithubOAuth2',  # for Github authentication
    'social_core.backends.facebook.FacebookOAuth2',  # for Facebook authentication

    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'GandharvaWeb19.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "EventApp/static")
# ]

# INSTAMOJO_KEY = '3ec2051ed0ae46ae17db917ee1ea381b'
# INSTAMOJO_AUTH_TOKEN = 'b80aafa7472907fbd0b60a3861c5731f' b80aafa7472907fbd0b60a3861c5731f
# INSTAMOJO_SALT = 'dc3ff23932af4594aa376c3793d803fe'

# INSTAMOJO_KEY = 'test_faf65f582c906177257c757e6cd'
# INSTAMOJO_AUTH_TOKEN = 'test_6ad0a420610b722f76d5437da00'
# INSTAMOJO_SALT = '924b7e87c0924c7e87224e698a829825'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '941888329527-bknhunrj63gk5id2ibhtd1ou4hv4bkc7.apps.googleusercontent.com'  # Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'FSqq7HvDDkZucHi0Wr-EHVuu'  # Paste Secret Key

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'viitgandharva3@gmail.com'


# EMAIL_HOST_PASSWORD = 'GandharvaViitPune@19'http://127.0.0.1:8000/
EMAIL_PORT = 587

MEDIA_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR, '')

USE_HTTPS = False
