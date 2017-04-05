# -*- coding: utf-8 -*-
from main.celery_app import app as celery_app
from celery.utils.log import get_task_logger
from water.utils import send_email_for_test

logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def celery_test(self,  **kwargs):
    pass


@celery_app.task(bind=True)
def celery_send_email_for_test(self,  **kwargs):
    send_email_for_test()
