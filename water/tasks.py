# -*- coding: utf-8 -*-
import json
from main.celery_app import app as celery_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery_app.task(bind=True)
def celery_test(self,  **kwargs):
    pass
