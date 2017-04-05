from __future__ import absolute_import
import os
import celery
from django.conf import settings
import raven
from raven.contrib.celery import register_signal, register_logger_signal

# set the default Django settings module for the 'celery' program.
INCLUDED_TASKS = [
    'water.tasks',
]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')


class Celery(celery.Celery):

    def on_configure(self):
        client = raven.Client("%s" %
                              settings.RAVEN_CONFIG['dsn'])

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)


app = Celery(
    'hmapps_worker', broker=settings.BROKER_URL, include=INCLUDED_TASKS)
app.config_from_object('django.conf:settings')
