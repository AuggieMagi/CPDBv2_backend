from .common import *  # NOQA


INSTALLED_APPS += ('django_extensions',)  # NOQA

CORS_ORIGIN_WHITELIST = (
    'localhost:9966',
    'localhost:9967',
    )

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MEDIA_ROOT = '/www/media/'
DOMAIN = 'http://localhost:9966'

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
