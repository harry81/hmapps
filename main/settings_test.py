try:
    from settings import *
    from django.conf import settings
except:
    pass

if 'live' in settings.DATABASES:
    settings.DATABASES.pop('live')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
CELERY_ALWAYS_EAGER = True
