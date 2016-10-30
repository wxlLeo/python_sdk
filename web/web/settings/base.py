# -*- coding: utf-8 -*-

import os
import sys




BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = BASE_DIR

ENV_DEV = "dev"
ENV_TEST = "test"
ENV_WWW = "www"

ENV = ENV_DEV

SECRET_KEY = 'fanlitou'

STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    # other finders..
)


# SECURITY WARNING: don't run with debug turned on in production!
if ENV in [ENV_WWW, ENV_TEST]:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['.fanlitou.cn', "127.0.0.1", "localhost", ".fanlitou.com"]
SECURE_PROXY_SSL_HEADER = ('HTTP_D_FORWARDED_SCHEME', 'https')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    "rest_framework",

    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'web.urls'
URLCONF_EXT = []


WSGI_APPLICATION = 'web.wsgi.application'


CER_ROOT = "certificate"

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# modified by Haiping to enable compare between offset-naive and offset-aware datetimes
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)






SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600
# enable crosssite session
SESSION_COOKIE_DOMAIN = '.fanlitou.com'
SESSION_COOKIE_NAME = 'session_id'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/tmp/flt_web.log',
            'when': 'MIDNIGHT',  # S - Seconds
                        # M - Minutes
                        # H - Hours
                        # D - Days 注意配置为D可能会产生隔天服务重启未生成新log的问题,应该使用MIDNIGTH
                        # MIDNIGHT - roll over at midnight 需注意与D的区别
                        # W{0-6} - roll over on a certain day; 0 - Monday
            'backupCount': 7,
            'encoding': 'utf8',
            'interval': 1,  # 间隔
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'web': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
        },
        'api': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
        },
    },
}



LOCAL_SETTING = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings_local.py")
if os.path.isfile(LOCAL_SETTING):
    execfile(LOCAL_SETTING)


# unit test {{{
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': ':memory:',
        },
    }
    SOUTH_TESTS_MIGRATE = False
    SKIP_SOUTH_TESTS = True
# unit test }}}
