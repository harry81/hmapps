# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand
from water.utils import (fetch_news_to_S3,
                         load_from_S3, send_email_for_test)

reload(sys)
sys.setdefaultencoding('utf-8')


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        # fetch_news_to_S3()
        articles = load_from_S3()
        send_email_for_test(articles)
