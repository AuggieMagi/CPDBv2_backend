from .common import *  # NOQA
from .common import APPS_DIR, INSTALLED_APPS


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
MEDIA_ROOT = str(APPS_DIR('test_media'))
TEST = True

NOSE_PLUGINS = [
    'snapshot_test.plugins.CreateSnapshotPlugin',
    'snapshot_test.plugins.CleanupDirIfSuccessPlugin'
]

INSTALLED_APPS += ('snapshot_test',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {},
    'handlers': {},
    'loggers': {}
}


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

DOMAIN = 'http://foo.com'

TWITTERBOT_ENV = 'test'

V1_URL = 'http://cpdb.lvh.me'
