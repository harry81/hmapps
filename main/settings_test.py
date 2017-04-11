try:
    from settings import *
except:
    pass

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
CELERY_ALWAYS_EAGER = True
