# -*- coding: utf-8 -*-
from main.celery_app import app as celery_app
from celery.utils.log import get_task_logger
from water.utils import (fetch_news_to_S3,
                         load_from_S3,
                         send_email_for_fetched_articles)

logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def celery_test(self,  **kwargs):
    pass


@celery_app.task(bind=True)
def celery_send_email_for_fetched_articles(self,  **kwargs):
    fetch_news_to_S3()
    articles = load_from_S3()
    send_email_for_fetched_articles(articles)
