from main.settings import *

if 'live' in DATABASES:
    DATABASES.pop('live')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
CELERY_ALWAYS_EAGER = True
