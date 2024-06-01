from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
from beaker.cache import cache_regions
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(find_dotenv(), override=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd Parties
    'ckeditor',
    'ckeditor_uploader',

    # Apps
    'utils',
    'blog_users',
    'blogging'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blogs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [f'{BASE_DIR}/blogs/templates'],
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

WSGI_APPLICATION = 'blogs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ["DB_DEFAULT_ENGINE"],
        "NAME": os.environ["DB_DEFAULT_NAME"],
        "USER": os.environ["DB_DEFAULT_USER"],
        "PASSWORD": os.environ["DB_DEFAULT_PASSWORD"],
        "HOST": os.environ["DB_DEFAULT_HOST"],
        "PORT": os.environ["DB_DEFAULT_PORT"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'blog_users.User'

CKEDITOR_UPLOAD_PATH = "image_upload/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format', 'Font', 'FontSize'],
            ['Bold', 'Italic', 'Underline'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['CodeSnippet', 'RemoveFormat', 'Source'],
            {
                'name': 'forms',
                'items': [
                    'Form',
                    'Checkbox',
                    'Radio',
                    'TextField',
                    'Textarea',
                    'Select',
                    'Button',
                    'ImageButton',
                    'HiddenField'
                ]
            },
            {
                'name': 'result', 
                'items': [
                    'Preview',
                    'Maximize',
                ]
            },
        ],
        'extraPlugins': ','.join(['codesnippet']),
    }
}


# configure regions
cache_regions.update({
    '5_min': {
        'expire': 5 * 60,
        'type': 'ext:redis',
        'url': os.environ["REDIS_HOST"],
    },
    '10_min': {
        'expire': 10 * 60,
        'type': 'ext:redis',
        'url': os.environ["REDIS_HOST"],
    },
    '30_min': {
        'expire': 30 * 60,
        'type': 'ext:redis',
        'url': os.environ["REDIS_HOST"],
    },
    '1_hour': {
        'expire': 60 * 60,
        'type': 'ext:redis',
        'url': os.environ["REDIS_HOST"],
    }
})


# DRF Configs
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=30)
}
