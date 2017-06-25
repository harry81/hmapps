# -*- coding: utf-8 -*-
from main.celery_app import app as celery_app
from celery.utils.log import get_task_logger
from .utils import update_deals

logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def celery_load_deals(self,  **kwargs):
    update_deals(**kwargs)
